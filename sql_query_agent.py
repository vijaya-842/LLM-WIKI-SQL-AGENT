"""Natural-language -> SQL agent that grounds itself in the Markdown wiki pages
produced by wiki_agent.py, instead of hitting the live database schema directly.

Flow:
1. Read wiki/index.md, the wiki's navigation catalog (links + one-line summaries
   for every entity, relationship, domain, enum, and canonical query/analysis page).
2. Ask the OpenAI model which of those pages it needs to read to answer the question —
   this is what lets the agent pull in a `wiki/queries/*.md` page documenting a past
   mistake, or a `wiki/relationships/*.md` page, not just entity pages.
3. Read exactly those pages from disk.
4. Ask the model to write one SQL query grounded only in what those pages say.
5. Optionally execute the query (SELECT-only) against Postgres and return rows.

Uses the OpenAI API (OPENAI_API_KEY from the environment / .env) rather than the local Ollama
model wiki_agent.py still uses for wiki generation — the two are independent.
"""

import json
import os
import re
from datetime import date

from groq import Groq

import db_introspect as db
from dbconnection import get_connection  # importing this also triggers dbconnection's load_dotenv(),
# which is what makes OPENAI_API_KEY (set in .env) visible to the OpenAI() client below.

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "qwen/qwen3.8-27b"  
# Wiki navigation is a cheap, high-volume tool-calling loop (keyword search + page reads) where a
# wrong pick just means one extra read_wiki_page round trip. Writing/correcting SQL is where actual
# schema reasoning happens (e.g. spotting that a dollar amount is derived on a line-item table
# rather than stored on the header table) and is where a weaker model's mistakes turn into
# validation failures or, worse, silently-wrong SQL — so it gets its own, stronger-by-default model.
NAV_MODEL = os.environ.get("GROQ_NAV_MODEL", MODEL)
SQL_MODEL = os.environ.get("GROQ_SQL_MODEL", MODEL)



def _chat(messages, tools=None, model=None):
    """Thin wrapper around the OpenAI chat completions call, used everywhere this module needs a
    model response. Returns the raw ChatCompletionMessage (has .content and .tool_calls)."""
    kwargs = {"model": model or MODEL, "messages": messages, "max_tokens": 500}
    if tools:
        kwargs["tools"] = tools
    response = _client.chat.completions.create(**kwargs)
    return response.choices[0].message
WIKI_DIR = os.path.join(os.path.dirname(__file__), "wiki")
INDEX_PATH = os.path.join(WIKI_DIR, "index.md")
ENTITIES_DIR = os.path.join(WIKI_DIR, "entities")
CORRECTIONS_PATH = os.path.join(WIKI_DIR, "corrections.md")

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")
MISSING_COLUMN_RE = re.compile(r"does not exist on table `(\w+)`")
MISSING_TABLE_RE = re.compile(r"table `(\w+)` referenced in FROM/JOIN does not exist in the schema")
MAX_CORRECTION_ATTEMPTS = 2


def _extract_missing_table(reason):
    """Pull the table name a validation failure is about, from either error shape
    db_introspect.validate_query_sql produces: a bad column on a real table ('does not exist on
    table `X`') or a fully invented table/join target ('table `X` ... does not exist in the
    schema'). Returns None if the reason matches neither shape."""
    if not reason:
        return None
    match = MISSING_COLUMN_RE.search(reason) or MISSING_TABLE_RE.search(reason)
    return match.group(1) if match else None


def load_entity_docs():
    """Read every table's entity page into {table_name: full_markdown_text}. Used by the UI to
    list/browse tables — generate_sql() itself no longer uses this; it navigates from
    wiki/index.md and can pull in any page, not just entities/."""
    docs = {}
    if not os.path.isdir(ENTITIES_DIR):
        return docs
    for filename in sorted(os.listdir(ENTITIES_DIR)):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(ENTITIES_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            docs[filename[:-3]] = f.read()
    return docs


def load_index():
    """Read wiki/index.md — the entry point for navigation, per the wiki's own rules
    ('Start from wiki/index.md')."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _wikilink_to_path(link):
    """Resolve an Obsidian-style wikilink target (e.g. 'entities/vendor_pricing', 'erd')
    to its file path under wiki/. Raises ValueError if the resolved path would escape
    WIKI_DIR (e.g. via '../' segments), since this is used to sandbox tool-driven reads
    to the wiki directory only."""
    link = link.strip().split("#", 1)[0].strip()
    path = os.path.normpath(os.path.join(WIKI_DIR, *link.split("/")) + ".md")
    if os.path.commonpath([path, WIKI_DIR]) != os.path.normpath(WIKI_DIR):
        raise ValueError(f"Path '{link}' resolves outside the wiki directory.")
    return path


def load_wiki_page(link):
    """Read one wiki page by its wikilink target. Returns None if the model named a
    page that doesn't actually exist (hallucinated link) or the link escapes wiki/."""
    try:
        path = _wikilink_to_path(link)
    except ValueError:
        return None
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _iter_wiki_pages():
    """Yield (wikilink, full_text) for every markdown page under WIKI_DIR."""
    for root, _dirs, files in os.walk(WIKI_DIR):
        for filename in sorted(files):
            if not filename.endswith(".md"):
                continue
            path = os.path.join(root, filename)
            link = os.path.relpath(path, WIKI_DIR)[: -len(".md")].replace(os.sep, "/")
            with open(path, "r", encoding="utf-8") as f:
                yield link, f.read()


def search_wiki(query, max_results=8):
    """Keyword search over every wiki page's title/headings/body. Sandboxed to WIKI_DIR —
    it only ever reads files under wiki/. Returns a list of {"page": wikilink, "snippet": str}
    for pages containing the query (case-insensitive), ranked by number of matches. Used as a
    tool so the model can find a page navigation from index.md alone might miss (e.g. it knows
    a column name but not which entity page documents it)."""
    query_lower = query.strip().lower()
    if not query_lower:
        return []
    results = []
    for link, text in _iter_wiki_pages():
        text_lower = text.lower()
        count = text_lower.count(query_lower)
        if count == 0:
            continue
        idx = text_lower.find(query_lower)
        start = max(0, idx - 60)
        end = min(len(text), idx + len(query_lower) + 60)
        snippet = text[start:end].replace("\n", " ").strip()
        results.append((count, link, snippet))
    results.sort(key=lambda r: r[0], reverse=True)
    return [{"page": link, "snippet": snippet} for _count, link, snippet in results[:max_results]]


def read_wiki_page(path):
    """Tool wrapper around load_wiki_page for the tool-calling loop: returns a plain string
    (the page text, or an error message) instead of None, since tool results must be strings."""
    text = load_wiki_page(path)
    if text is None:
        return f"No wiki page found at '{path}'."
    return text


def _extract_section(markdown_text, heading):
    pattern = rf"##\s*{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)"
    match = re.search(pattern, markdown_text, re.DOTALL)
    return match.group(1).strip() if match else ""


def page_context(link, markdown_text):
    """Build prompt context for one selected wiki page. Entity pages (identified by having
    a Column Reference Table section) are condensed to overview + columns + examples + gotchas,
    so token budget stays low even with several tables in play while still keeping the two
    sections that actually prevent repeat mistakes: Common Query Examples (a worked, correct
    query for that table) and Known Query Gotchas (past validation failures recorded against
    this exact table). Dropping those two — as an earlier version of this function did — meant
    the model saw a table's columns but never the worked example or the note that a previous
    attempt at the same question already failed, so it kept re-making the same mistake even
    when the right entity page was in context. Other pages — relationships, canonical
    query/analysis pages, domains, enums — are already short and are included in full.

    Headings intentionally avoid the raw 'entities/foo' wikilink form — a model reading
    'entities/vendor_pricing' as a heading has been observed writing `FROM entities.vendor_pricing`,
    mistaking the wiki path for a schema-qualified table name."""
    columns = _extract_section(markdown_text, "Column Reference Table")
    if columns:
        table_name = link.rsplit("/", 1)[-1]
        overview = _extract_section(markdown_text, "Overview")
        context = f"### Table: {table_name}\n{overview}\n\n{columns}\n"
        examples = _extract_section(markdown_text, "Common Query Examples")
        if examples:
            context += f"\n#### Example queries against `{table_name}`\n{examples}\n"
        gotchas = _extract_section(markdown_text, "Known Query Gotchas")
        if gotchas:
            context += f"\n#### Past mistakes on `{table_name}` — do not repeat these\n{gotchas}\n"
        return context
    return f"### Reference page ({link})\n{markdown_text.strip()}\n"


def _entity_names():
    """All real table names, derived from wiki/entities/*.md filenames — the ground truth for
    splitting a relationship page's filename back into its two table names below."""
    if not os.path.isdir(ENTITIES_DIR):
        return set()
    return {f[:-3] for f in os.listdir(ENTITIES_DIR) if f.endswith(".md")}


def _tables_from_relationship_link(link):
    """Given a 'relationships/X-Y' wikilink, recover the two real table names its filename
    documents (e.g. 'site_vendor_assignments-sites' -> ['site_vendor_assignments', 'sites']).
    Table names themselves only ever contain letters/digits/underscores, never '-', so trying
    each '-'-split point until both halves are real table names is unambiguous. Returns [] for
    non-relationship links or ones with no valid split (e.g. 'relationships/overview')."""
    if not link.startswith("relationships/"):
        return []
    name = link[len("relationships/"):]
    valid = _entity_names()
    parts = name.split("-")
    for i in range(1, len(parts)):
        left, right = "-".join(parts[:i]), "-".join(parts[i:])
        if left in valid and right in valid:
            return [left, right]
    return []


def _expand_with_linked_entities(pages, max_pages):
    """A relationship page documents that a join exists but not the full column list of either
    side; a query/analysis page links to the entities it queries. Whatever the navigation step
    picked, follow the entity wikilinks those pages themselves contain and pull those entity
    pages in too — so the model always has ground-truth columns for every table it might touch,
    instead of depending on the navigation call happening to name the entity page directly.

    Also follows relationship-page links the same way: an entity page's own 'Related' section
    typically links to '[[relationships/A-B]]' rather than '[[entities/B]]' directly (e.g.
    purchase_orders.md links to relationships/purchase_order_lines-purchase_orders, never to
    entities/purchase_order_lines itself), so a plain entities/-prefix scan alone would never
    pull in a sibling table one hop away — which is exactly how a derived-amount table like
    purchase_order_lines went missing from context in a past failure even though purchase_orders
    (the table that doesn't have the amount) was right there."""
    candidate_links = set()
    for text in pages.values():
        for link in WIKILINK_RE.findall(text):
            link = link.strip()
            if link.startswith("entities/"):
                candidate_links.add(link)
            elif link.startswith("relationships/"):
                candidate_links.update(f"entities/{t}" for t in _tables_from_relationship_link(link))

    for link in candidate_links:
        if len(pages) >= max_pages:
            break
        if link in pages:
            continue
        entity_text = load_wiki_page(link)
        if entity_text is not None:
            pages[link] = entity_text
    return pages


NAVIGATE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_wiki",
            "description": (
                "Keyword search over every page in the wiki (titles, headings, and body text). "
                "Use this when you know a column, table, or concept name but aren't sure which "
                "page documents it, or when the index alone doesn't make the right page obvious."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keyword or short phrase to search for, e.g. a column or table name.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_wiki_page",
            "description": (
                "Read the full text of one wiki page by its wikilink path, e.g. 'entities/vendor_pricing' "
                "or 'relationships/overview'. Use this to pull in any page you've identified as relevant, "
                "whether from the index or from search_wiki results."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Wikilink path exactly as it appears in the index or in search_wiki results.",
                    }
                },
                "required": ["path"],
            },
        },
    },
]

NAVIGATE_TOOL_IMPLS = {"search_wiki": search_wiki, "read_wiki_page": read_wiki_page}

NAVIGATE_PROMPT = """You are navigating a Markdown wiki that documents a Postgres database, to \
answer a user's question. Below is the wiki's index page, which links to entity pages (one per \
real table), relationship pages (documenting foreign keys, including which column is an ID vs a \
name), domain pages, enum pages, and canonical query/analysis pages (which record past mistakes \
and their corrected SQL). relationships/overview.md — the full FK relationship graph for the whole \
schema — is already included in every request automatically; you do not need to read it yourself.

{index}

User question: "{question}"

IMPORTANT — multi-hop joins: many real questions need a table that has NO direct relationship page \
to the table the question is "about" (e.g. an item's shipping address may live on a table only \
connected to vendors, not to items, so answering it means chaining item -> pricing -> vendor -> \
shipping point through two intermediate relationship pages). Never conclude a question is \
unanswerable just because no single relationship page connects the two tables directly. Use the \
FK graph (visible in relationships/overview.md, already provided) to find an intermediate table \
that has a relationship to both sides, and read the entity and relationship pages for every table \
in that chain, not just the endpoints.

You have two tools: search_wiki(query) to find pages by keyword when the index alone doesn't make \
the right page obvious, and read_wiki_page(path) to read a page's full text. Call read_wiki_page \
for the entity page of every table you might query (including intermediate bridge tables), any \
relationship page for a join you might need, and any canonical query/analysis page whose title \
looks related to this question's shape, since those often correct a mistake a naive query would \
otherwise make. Keep calling tools until you've read everything you need, then reply with a final \
message (no more tool calls) that explains in 1-2 sentences which pages you used and why.
"""


def _run_tool_call(name, args):
    """Execute one model-requested tool call against NAVIGATE_TOOL_IMPLS and return its result
    as a string, ready to hand back to the model as a tool message."""
    impl = NAVIGATE_TOOL_IMPLS.get(name)
    if impl is None:
        return f"Unknown tool '{name}'."
    try:
        result = impl(**args)
    except Exception as e:
        return f"Tool '{name}' failed: {e}"
    return result if isinstance(result, str) else str(result)


def select_relevant_pages(question, index_text, max_pages=8, max_tool_rounds=6):
    """Run a tool-calling loop where the model can search_wiki() and read_wiki_page() as many
    times as it needs, instead of committing to a page list from the index alone. Returns
    (pages, reasoning) where pages is {wikilink: full_text} for every page actually read via
    read_wiki_page, capped at max_pages. Falls back to the first entity links in the index if
    the model never calls read_wiki_page (e.g. a model that ignores tools entirely)."""
    messages = [{"role": "user", "content": NAVIGATE_PROMPT.format(index=index_text, question=question)}]
    pages = {}
    reasoning = ""

    for _round in range(max_tool_rounds):
        message = _chat(messages, tools=NAVIGATE_TOOLS, model=NAV_MODEL)
        messages.append(message.model_dump(exclude_none=True))

        tool_calls = message.tool_calls or []
        if not tool_calls:
            reasoning = (message.content or "").strip()
            break

        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            result = _run_tool_call(name, args)
            if name == "read_wiki_page" and len(pages) < max_pages:
                path = args.get("path", "").strip()
                if path and load_wiki_page(path) is not None:
                    pages[path] = result
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

    if pages:
        return pages, reasoning or "(model did not explain its page choices)"

    fallback_links = WIKILINK_RE.findall(index_text)[:max_pages]
    fallback_pages = {link: text for link in fallback_links if (text := load_wiki_page(link)) is not None}
    return (
        fallback_pages,
        "Navigation step never called read_wiki_page; defaulted to the first entity pages in the index.",
    )


SQL_PROMPT = """You are a SQL assistant for a Postgres database. Below is documentation for the \
relevant tables, taken from the team's data wiki. Use ONLY the tables and columns shown here — \
never invent a column or table name that doesn't appear below.

The ONLY real tables in this schema are: {valid_tables}. Do not reference any table not in this \
list, even if it sounds plausible (e.g. a table named after the concept in the question).

{schema_context}
{prior_mistakes}
User question: "{question}"

First, in 1-2 sentences, explain which table(s)/columns you're using and why, referencing the \
wiki pages above by name. Then write a single Postgres SQL query that answers the question, in \
a ```sql fenced code block.
"""


def _extract_sql(response_text):
    match = re.search(r"```sql\s*\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\s*\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text.strip()


def _extract_explanation(response_text):
    """The prose the model wrote before its ```sql fence — the 'why' behind the query, for
    display in the UI. Empty string if the model skipped straight to the fence."""
    fence_pos = response_text.find("```")
    return response_text[:fence_pos].strip() if fence_pos > 0 else ""


CORRECTION_PROMPT = """Your previous answer(s) to this question used a table or column that does \
not exist in the schema:

{previous_attempts}

The ONLY real tables in this schema are: {valid_tables}. Do not repeat any of the rejected \
queries above, and do not reference any table not in this list.

{schema_context}

User question: "{question}"

First, in 1 sentence, explain what was wrong and how you're fixing it. Then rewrite the query \
using ONLY the tables and columns shown above, in a ```sql fenced code block.
"""


CORRECTION_BLOCK_RE = re.compile(
    r"^## \[[\d-]+\] (?P<table>\S+) — validation failed.*?\n(?P<body>.*?)(?=\n## \[|\Z)",
    re.DOTALL | re.MULTILINE,
)


def _prior_corrections_context(question, tables, max_entries=3):
    """Look up wiki/corrections.md for previous validation failures relevant to THIS question, so
    the model gets a warning about known-bad SQL *before* it generates anything, instead of only
    via wiki_agent.py's next regeneration pass (which may not have run yet).

    Matched by which real tables are already in context (schema-level), not by exact question
    text — a rephrased question that touches the same table ('gap between what they buy and
    sell' vs 'compare PO totals to invoice totals') still surfaces the warning this way, where the
    old exact-string match would miss it entirely and let the same mistake repeat under a new
    phrasing. Also still matches on exact question text as a fallback, for entries whose table
    couldn't be identified (logged as 'unknown-table'). `tables` is the set of real table names
    already selected as context (from `pages`, entities/-prefixed links). Returns "" if the file
    doesn't exist or nothing matches."""
    if not os.path.isfile(CORRECTIONS_PATH):
        return ""
    with open(CORRECTIONS_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    normalized_question = re.sub(r"\s+", " ", question).strip().lower()
    matches = []
    for block_match in CORRECTION_BLOCK_RE.finditer(text):
        table, body = block_match.group("table"), block_match.group("body")
        q_match = re.search(r'Question:\s*"([^"]*)"', body)
        same_question = bool(q_match) and (
            re.sub(r"\s+", " ", q_match.group(1)).strip().lower() == normalized_question
        )
        if table not in tables and not same_question:
            continue
        rejected_match = re.search(r"Rejected SQL:\s*`([^`]*)`", body)
        outcome_match = re.search(r"Outcome[^:]*:\s*(.*)", body)
        matches.append(
            f"- On `{table}`: rejected `{rejected_match.group(1) if rejected_match else '(unknown)'}`\n"
            f"  Outcome: {outcome_match.group(1).strip() if outcome_match else '(unknown)'}"
        )

    if not matches:
        return ""
    return (
        "\nPast questions touching these same tables previously produced INVALID SQL. "
        "Do not repeat these mistakes:\n" + "\n".join(matches[-max_entries:]) + "\n"
    )


def _log_correction(question, pages_used, attempts, resolved):
    """Append a record of a SQL validation failure to wiki/corrections.md, so wiki_agent.py can
    read it back on its next regeneration pass and strengthen whichever page left a gap — e.g. a
    relationship page that was selected without its entity page's column list ever making it into
    context. This is the query-time-failure -> wiki-generation feedback loop.

    `attempts` is the ordered list of (sql, reason) tuples for every rejected try (the final
    resolved/still-broken query is passed separately via `resolved`'s companion final sql, which
    is attempts[-1] when unresolved, or the caller's successful sql otherwise)."""
    first_sql, first_reason = attempts[0]
    final_sql, _ = attempts[-1]
    table = _extract_missing_table(first_reason) or "unknown-table"
    entity_page = f"entities/{table}"
    had_entity_page = entity_page in pages_used

    attempts_text = "\n".join(
        f"  {i}. `{' '.join(sql.split())}` — {reason}" for i, (sql, reason) in enumerate(attempts, 1)
    )

    entry = (
        f"\n## [{date.today().isoformat()}] {table} — validation failed on first attempt\n\n"
        f"- Question: \"{question}\"\n"
        f"- Wiki pages used: {', '.join(pages_used)}\n"
        f"- Rejected SQL: `{' '.join(first_sql.split())}`\n"
        f"- Validation error: {first_reason}\n"
        f"- All rejected attempts:\n{attempts_text}\n"
        f"- Outcome after {len(attempts) - 1} correction attempt(s): {'fixed' if resolved else 'STILL BROKEN'} — "
        f"`{' '.join(final_sql.split())}`\n"
        f"- Suggested wiki fix: "
        + (
            f"`{entity_page}` was NOT among the pages used, so its real column list wasn't in "
            f"context when the query was written — check whether pages linking to `{table}` "
            f"surface its key columns directly.\n"
            if not had_entity_page
            else f"`{entity_page}` WAS in context but the model still invented a column/table — check "
            f"whether its Column Reference Table, Common Query Examples, or Known Query Gotchas "
            f"clearly distinguish similarly-named columns.\n"
        )
    )

    if not os.path.isfile(CORRECTIONS_PATH):
        with open(CORRECTIONS_PATH, "w", encoding="utf-8") as f:
            f.write(
                "# Corrections Log\n\nAppend-only record of SQL validation failures from "
                "`sql_query_agent.py`, for `wiki_agent.py` to review on its next regeneration "
                "pass and address the documentation gap that caused each one.\n"
            )
    with open(CORRECTIONS_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


def _collect_initial_pages(pages, max_pages):
    """Finalize the {link: text} context the navigation tool-loop already read:
    relationships/overview.md is always included so the model always sees the full FK graph, \
    regardless of what navigation picked — a small local model reliably keyword-matches the \
    obvious table but misses that the answer actually requires an intermediate bridge table it \
    never named. Every page's [[entities/...]] wikilinks also feed _expand_with_linked_entities, \
    so a bridge table's real columns get pulled in even when navigation never read that table \
    itself."""
    pages = dict(pages)
    if "relationships/overview" not in pages and len(pages) < max_pages:
        overview_text = load_wiki_page("relationships/overview")
        if overview_text is not None:
            pages["relationships/overview"] = overview_text
    return _expand_with_linked_entities(pages, max_pages)


def _related_entity_links(table):
    """Every other real table connected to `table` via a relationship page (one hop out), e.g.
    'purchase_orders' -> {'entities/purchase_order_lines', 'entities/vendors', 'entities/sites', ...}.
    Used when a correction retry needs to discover a table it never had in context at all — e.g. a
    dollar amount that's derived on a line-item table rather than stored as a column on the header
    table it guessed on — since re-reading the header table's own page again teaches it nothing new."""
    links = set()
    for link, _text in _iter_wiki_pages():
        tables = _tables_from_relationship_link(link)
        if table in tables:
            links.update(f"entities/{t}" for t in tables if t != table)
    return links


def _attempt_correction(question, reason, pages, schema_columns, rejected_attempts, max_pages=12):
    """Self-heal one validation failure. Returns (new_sql, new_explanation, is_valid, reason, pages).

    Two distinct failure shapes need two distinct fixes:
    - The error names a real table whose entity page wasn't already in context (e.g. the model
      invented a join to a table it never saw the columns for): pull that page in now.
    - The error is a bad *column* on a table whose entity page WAS already in context (e.g.
      `po.total_amount does not exist on table purchase_orders`, where purchase_orders was right
      there and simply doesn't have that column): re-showing the same page teaches the retry
      nothing, and it tends to just re-guess a different wrong column on the same table. What's
      actually missing is a *different* table one hop away (here, purchase_order_lines, which
      holds the derived amount) that navigation never had reason to read. So in this case, pull in
      every table connected to the offending one via a relationship page, so the retry can
      discover the real answer instead of guessing again blind.

    Also passes the full list of every attempt rejected so far (not just the latest) and the
    closed list of real table names, so a retry can't repeat an earlier mistake or invent yet
    another table that was never a real option."""
    table = _extract_missing_table(reason)
    if table:
        entity_link = f"entities/{table}"
        is_bad_column = bool(MISSING_COLUMN_RE.search(reason or ""))
        if entity_link not in pages:
            entity_text = load_wiki_page(entity_link)
            if entity_text is not None:
                pages[entity_link] = entity_text
        elif is_bad_column:
            for link in sorted(_related_entity_links(table)):
                if len(pages) >= max_pages:
                    break
                if link in pages:
                    continue
                text = load_wiki_page(link)
                if text is not None:
                    pages[link] = text

    schema_context = "\n".join(page_context(l, t) for l, t in pages.items())
    previous_attempts = "\n".join(
        f"Attempt {i}: `{' '.join(s.split())}` — rejected: {r}"
        for i, (s, r) in enumerate(rejected_attempts, 1)
    )
    correction = CORRECTION_PROMPT.format(
        previous_attempts=previous_attempts,
        valid_tables=", ".join(sorted(schema_columns.keys())),
        schema_context=schema_context,
        question=question,
    )
    content = _chat([{"role": "user", "content": correction}], model=SQL_MODEL).content
    new_sql = _extract_sql(content)
    new_explanation = _extract_explanation(content)
    is_valid, new_reason = db.validate_query_sql(new_sql, schema_columns)
    return new_sql, new_explanation, is_valid, new_reason, pages


def generate_sql(question, max_pages=8, max_correction_attempts=MAX_CORRECTION_ATTEMPTS):
    """Return a dict describing how the agent answered a natural-language question, grounded in
    wiki pages the model chose to navigate to from wiki/index.md:
        sql                 - the generated SQL
        pages_used          - wikilinks of every page actually in context (navigation picks +
                               auto-expanded entity pages + anything pulled in during correction)
        navigation_reasoning- the model's own explanation of why it picked those pages
        sql_explanation     - the model's own explanation of which tables/columns it used and why
        corrected           - True if the first attempt failed validation and had to be retried
    Validates the generated SQL against the live schema and gives the model up to
    `max_correction_attempts` chances to correct itself if it invented a table/column (e.g.
    leaking a column name from a different table), raising instead of silently handing back SQL
    that will fail (or worse, quietly succeed against the wrong column) once it's run against
    Postgres. Each retry sees every previously rejected attempt, not just the last one, so it
    can't cycle back to a mistake it already made."""
    index_text = load_index()
    navigated_pages, navigation_reasoning = select_relevant_pages(question, index_text, max_pages=max_pages)

    pages = _collect_initial_pages(navigated_pages, max_pages)
    if not pages:
        raise RuntimeError(
            f"Navigation step selected no valid wiki pages for question: {question!r}. "
            f"Run wiki_agent.py first if wiki/ is empty."
        )

    schema_context = "\n".join(page_context(link, text) for link, text in pages.items())
    schema_columns = db.get_schema_columns()  # validate against the full live schema, not just pages
    context_tables = {link.rsplit("/", 1)[-1] for link in pages if link.startswith("entities/")}

    prompt = SQL_PROMPT.format(
        valid_tables=", ".join(sorted(schema_columns.keys())),
        schema_context=schema_context,
        prior_mistakes=_prior_corrections_context(question, context_tables),
        question=question,
    )
    content = _chat([{"role": "user", "content": prompt}], model=SQL_MODEL).content
    sql = _extract_sql(content)
    sql_explanation = _extract_explanation(content)

    corrected = False
    is_valid, reason = db.validate_query_sql(sql, schema_columns)
    if not is_valid:
        corrected = True
        pages_used_on_first_attempt = list(pages.keys())
        rejected_attempts = [(sql, reason)]

        for _attempt in range(max_correction_attempts):
            sql, new_explanation, is_valid, reason, pages = _attempt_correction(
                question, reason, pages, schema_columns, rejected_attempts, max_pages=max_pages + 4
            )
            sql_explanation = new_explanation or sql_explanation
            if is_valid:
                break
            rejected_attempts.append((sql, reason))

        _log_correction(question, pages_used_on_first_attempt, rejected_attempts, is_valid)

        if not is_valid:
            raise ValueError(
                f"Generated SQL still references a nonexistent table/column after "
                f"{max_correction_attempts} correction attempt(s) ({reason}). Last attempt:\n{sql}"
            )

    return {
        "sql": sql,
        "pages_used": list(pages.keys()),
        "navigation_reasoning": navigation_reasoning,
        "sql_explanation": sql_explanation,
        "corrected": corrected,
    }


def run_sql(sql, limit=200):
    """Execute any SQL statement and return (columns, rows). For statements that return no
    result set (INSERT/UPDATE/DELETE/DDL/etc.), columns and rows are both empty and the
    transaction is committed."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchmany(limit)
            else:
                columns, rows = [], []
            conn.commit()
            return columns, rows
    finally:
        conn.close()


if __name__ == "__main__":
    q = input("Ask a question about the data: ")
    result = generate_sql(q)
    print(f"\n[pages used] {result['pages_used']}")
    print(f"\n[why these pages] {result['navigation_reasoning']}")
    print(f"\n[why this sql] {result['sql_explanation']}")
    print(f"\n[generated sql]\n{result['sql']}\n")
    cols, rows = run_sql(result["sql"])
    print(cols)
    for r in rows:
        print(r)
