import json
import os
import re
import time   
from datetime import date

from dotenv import load_dotenv
from groq import Groq

import db_introspect as db

load_dotenv()

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = os.environ.get("GROQ_MODEL", "qwen/qwen3.8-27b")

WIKI_DIR = os.path.join(os.path.dirname(__file__), "wiki")
ENTITIES_DIR = os.path.join(WIKI_DIR, "entities")
RELATIONSHIPS_DIR = os.path.join(WIKI_DIR, "relationships")
DOMAINS_DIR = os.path.join(WIKI_DIR, "domains")
ENUMS_DIR = os.path.join(WIKI_DIR, "enums")
QUERIES_DIR = os.path.join(WIKI_DIR, "queries")
INDEX_PATH = os.path.join(WIKI_DIR, "index.md")
LOG_PATH = os.path.join(WIKI_DIR, "log.md")
OVERVIEW_PATH = os.path.join(WIKI_DIR, "overview.md")
GLOSSARY_PATH = os.path.join(WIKI_DIR, "glossary.md")
CONVENTIONS_PATH = os.path.join(WIKI_DIR, "conventions.md")
ERD_PATH = os.path.join(WIKI_DIR, "erd.md")
RELATIONSHIPS_OVERVIEW_PATH = os.path.join(RELATIONSHIPS_DIR, "overview.md")
CLAUDE_MD_PATH = os.path.join(os.path.dirname(__file__), "claude.md")
CORRECTIONS_PATH = os.path.join(WIKI_DIR, "corrections.md")
CORRECTIONS_ARCHIVE_PATH = os.path.join(WIKI_DIR, "corrections_archive.md")

for _dir in (ENTITIES_DIR, RELATIONSHIPS_DIR, DOMAINS_DIR, ENUMS_DIR, QUERIES_DIR):
    os.makedirs(_dir, exist_ok=True)


def ensure_scaffold():
    """Create the wiki/ layout claude.md mandates (index.md, log.md, overview.md, entities/) the
    first time this agent runs, so table pages land in a real wiki instead of a flat file dump."""
    today = date.today().isoformat()

    if not os.path.isfile(OVERVIEW_PATH):
        with open(OVERVIEW_PATH, "w", encoding="utf-8") as f:
            f.write(
                "---\n"
                "title: Overview\n"
                "type: overview\n"
                "status: active\n"
                f"created: {today}\n"
                f"updated: {today}\n"
                "source_paths:\n"
                "source_count: 0\n"
                "---\n\n"
                "# Overview\n\n"
                "This wiki documents the tables in the connected Postgres database, generated and "
                "kept current by `wiki_agent.py`. Start at [[index]] to browse entity pages.\n"
            )

    if not os.path.isfile(INDEX_PATH):
        # run_agent() always rebuilds this via update_index(); this stub only covers the case
        # where the wiki is inspected before the first full run.
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write("# Wiki Index\n\nNavigation catalog. Run `python wiki_agent.py` to populate.\n")

    if not os.path.isfile(LOG_PATH):
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("# Log\n")


def _parse_frontmatter(path):
    """Return (fields dict, body str) for an existing page, or ({}, '') if it doesn't exist yet."""
    if not os.path.isfile(path):
        return {}, ""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, match.group(2)


def relationship_filename(fk, all_fks=None):
    """Filename for one FK relationship: '<source>-<target>.md'. Falls back to including the
    column when a table pair has more than one distinct FK between them (disambiguation), since
    e.g. two tables could share both a direct and an indirect reference."""
    base = f"{fk['source_table']}-{fk['target_table']}"
    if not all_fks:
        return base
    same_pair = [
        f for f in all_fks if f["source_table"] == fk["source_table"] and f["target_table"] == fk["target_table"]
    ]
    if len(same_pair) <= 1:
        return base
    return f"{base}-{fk['source_column']}"


def render_relationship_frontmatter(fk, created):
    today = date.today().isoformat()
    source_table, target_table = fk["source_table"], fk["target_table"]
    title = f"{source_table} → {target_table} ({fk['source_column']})"
    return (
        "---\n"
        f"title: {title}\n"
        "type: concept\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        f"  - live-database:public.{source_table}\n"
        f"  - live-database:public.{target_table}\n"
        "source_count: 2\n"
        "---\n\n"
    )


def render_entity_frontmatter(table_name, created):
    today = date.today().isoformat()
    title = table_name.replace("_", " ").title()
    return (
        "---\n"
        f"title: {title}\n"
        "type: entity\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        f"  - live-database:public.{table_name}\n"
        "source_count: 1\n"
        "---\n\n"
    )


def _first_sentence(text, max_len=180):
    """First sentence of a block of prose, truncated to max_len chars. Used to turn an entity
    page's real Overview section into a navigation-useful index line — a generic 'documented from
    live schema + sample data' line for every table gives an LLM doing page navigation nothing to
    match a question's meaning against (it can only match the table name string), which is exactly
    why a question like 'shipping address' failed to surface vendor_shipping_points reliably."""
    text = " ".join(text.split())
    if not text:
        return ""
    match = re.search(r"^(.*?[.!?])(\s|$)", text)
    sentence = match.group(1) if match else text
    if len(sentence) > max_len:
        sentence = sentence[: max_len - 1].rsplit(" ", 1)[0].rstrip() + "…"
    return sentence


def update_index(table_names, all_fks, domains=None, enum_columns=None, queries=None, table_summaries=None):
    """Rebuild every navigation section of index.md from the current wiki contents."""
    domains = domains or []
    enum_columns = enum_columns or []
    queries = queries or []
    table_summaries = table_summaries or {}

    def section(heading, lines):
        body = "\n".join(lines) + ("\n" if lines else "")
        return f"\n## {heading}\n{body}"

    entity_lines = [
        f"- [[entities/{name}]] — "
        + (
            table_summaries[name]
            if table_summaries.get(name)
            else f"Postgres table `{name}`, documented from live schema + sample data."
        )
        for name in sorted(table_names)
    ]
    relationship_lines = []
    if all_fks:
        relationship_lines.append("- [[relationships/overview]] — schema-wide FK relationship catalog.")
        relationship_lines += [
            f"- [[relationships/{relationship_filename(fk, all_fks)}]] — "
            f"`{fk['source_table']}.{fk['source_column']}` → `{fk['target_table']}.{fk['target_column']}`"
            for fk in sorted(all_fks, key=lambda fk: (fk["source_table"], fk["target_table"]))
        ]
    domain_lines = [f"- [[domains/{d['slug']}]] — {d['description']}" for d in domains]
    enum_lines = [f"- [[enums/{col}]]" for col in sorted(enum_columns)]
    query_lines = [f"- [[queries/{q['slug']}]] — {q['title']}" for q in queries]
    reference_lines = ["- [[erd]] — full schema entity-relationship diagram.", "- [[glossary]] — business terms mapped to schema columns.", "- [[conventions]] — naming/timestamp/soft-delete patterns observed across the schema."]

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(
            "# Wiki Index\n\n"
            "Navigation catalog. See [[overview]] for context and `log.md` for history.\n"
            + section("Entities", entity_lines)
            + section("Relationships", relationship_lines)
            + section("Domains", domain_lines)
            + section("Enums", enum_lines)
            + section("Queries", query_lines)
            + section("Reference", reference_lines)
        )


def append_log_entry(operation, title, paths, summary):
    today = date.today().isoformat()
    entry = (
        f"\n## [{today}] {operation} | {title}\n\n"
        f"- Paths touched: {', '.join(paths)}\n"
        f"- {summary}\n"
    )
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


CORRECTION_ENTRY_RE = re.compile(
    r"^## \[(?P<date>\d{4}-\d{2}-\d{2})\] (?P<table>\S+) — validation failed on first attempt\n"
    r"\n"
    r"- Question: \"(?P<question>.*)\"\n"
    r"- Wiki pages used: (?P<pages>.*)\n"
    r"- Rejected SQL: `(?P<bad_sql>.*)`\n"
    r"- Validation error: (?P<reason>.*)\n"
    r"(?:- All rejected attempts:\n(?:.*\n)*?)?"
    r"- Outcome after \d+ correction attempt\(s\): (?P<outcome>.*)\n"
    r"- Suggested wiki fix: (?P<suggestion>.*)\n",
    re.MULTILINE,
)


def load_corrections():
    """Parse wiki/corrections.md (written by sql_query_agent.py whenever it had to self-correct a
    SQL validation failure) into {table_name: [entry, ...]}. This is the query-time-failure ->
    wiki-generation feedback loop: each entry names the exact table/column confusion a live query
    hit, so this run can fold that lesson back into the page that left the gap."""
    if not os.path.isfile(CORRECTIONS_PATH):
        return {}
    with open(CORRECTIONS_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    by_table = {}
    for m in CORRECTION_ENTRY_RE.finditer(text):
        by_table.setdefault(m.group("table"), []).append(m.groupdict())
    return by_table


def render_corrections_section(corrections):
    """Deterministically render logged sql_query_agent validation failures relevant to a page,
    so the note faithfully reflects what actually happened rather than being reconstructed (and
    possibly distorted) by the narrative LLM call. Returns '' if there's nothing to show."""
    if not corrections:
        return ""
    return "\n".join(
        f"- **{c['date']}** — question *\"{c['question']}\"* produced `{c['bad_sql']}`, which "
        f"failed validation ({c['reason']}). {c['suggestion']}"
        for c in corrections
    )


def archive_corrections():
    """Move consumed corrections.md content into corrections_archive.md and clear the working
    log, so lessons already folded into pages this run don't get re-applied or pile up forever."""
    if not os.path.isfile(CORRECTIONS_PATH):
        return
    with open(CORRECTIONS_PATH, "r", encoding="utf-8") as f:
        consumed = f.read()
    with open(CORRECTIONS_ARCHIVE_PATH, "a", encoding="utf-8") as f:
        f.write(consumed)
    os.remove(CORRECTIONS_PATH)


def load_claude_instructions():
    """Read claude.md (the repo's wiki schema/operating rules), if present, so the model's
    prompts can be grounded in it instead of only the ad hoc section list baked into this file."""
    if not os.path.isfile(CLAUDE_MD_PATH):
        return ""
    with open(CLAUDE_MD_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def save_wiki_page(table_name: str, content: str):
    """Save a finished Markdown entity page for a table to wiki/entities/, prefixing claude.md-style
    frontmatter. Preserves the original `created` date across reruns; only `updated` changes."""
    path = os.path.join(ENTITIES_DIR, f"{table_name}.md")
    existing_fields, _ = _parse_frontmatter(path)
    created = existing_fields.get("created") or date.today().isoformat()
    full_content = render_entity_frontmatter(table_name, created) + content
    with open(path, "w", encoding="utf-8") as f:
        f.write(full_content)
    return {"saved_to": path, "bytes_written": len(full_content.encode("utf-8"))}


TOOL_IMPLS = {
    "list_tables": db.list_tables,
    "get_table_details": db.get_table_details,
    "build_erd_mermaid": db.build_erd_mermaid,
    "get_migration_history": db.get_migration_history,
    "save_wiki_page": save_wiki_page,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_tables",
            "description": "List every table in the public schema of the connected Postgres database.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_table_details",
            "description": (
                "Fetch full documentation data for one table: column reference "
                "(name/type/nullability/default/comment), primary key, foreign keys, "
                "indexes, check constraints, table comment, row count estimate, and sample rows."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table to inspect."}
                },
                "required": ["table_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_erd_mermaid",
            "description": "Build a Mermaid erDiagram string covering all tables and foreign-key relationships in the schema.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_migration_history",
            "description": (
                "Check the database for a known migration-tracking table "
                "(alembic_version, schema_migrations, flyway_schema_history, django_migrations, "
                "knex_migrations, sequelize_meta) and return its recorded history, if any."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_wiki_page",
            "description": "Save a completed Markdown wiki page for one table to disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {"type": "string"},
                    "content": {"type": "string", "description": "Full Markdown content of the wiki page."},
                },
                "required": ["table_name", "content"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a database documentation agent. You have tools to inspect a live \
Postgres database and to save finished wiki pages to disk.

{claude_instructions_block}

Your job, each time you are invoked, is:

1. Call list_tables to see what tables exist.
2. For each table, call get_table_details to get its columns, keys, indexes, constraints, \
comment, row count, and sample rows.
3. Call build_erd_mermaid once to get the schema-wide entity relationship diagram.
4. Call get_migration_history once to see if migration tracking exists.
5. For each table, compose a complete Markdown wiki page with these sections, in this order:
   - # <table_name>
   - ## Overview (purpose of the table, inferred from its name, columns, and sample data)
   - ## Entity Relationship Diagram (a ```mermaid``` fenced block; use the relevant portion of \
the ERD from build_erd_mermaid, or note there are no foreign-key relationships if there are none)
   - ## Column Reference Table (a Markdown table: Column | Type | Nullable | Default | Description; \
write a short business-meaning description for each column, inferred from its name/type/sample values)
   - ## Business Rules (derived from CHECK constraints, NOT NULL constraints, defaults, and \
column naming/value patterns you observe in the sample rows; if none are enforced at the DB level, \
say so explicitly and list *inferred* conventions instead)
   - ## Common Query Examples (2-4 realistic SQL queries against this table, using its real column names)
   - ## Index Documentation (list each index, its columns, and whether it's unique; if there are \
no indexes beyond a default, say so and suggest 1-2 indexes that would make sense given the columns)
   - ## Migration History (report what get_migration_history found; if nothing was found, state \
plainly that this database has no migration-tracking table and the schema is undocumented in that regard)
6. Call save_wiki_page(table_name, content) with the finished Markdown for each table.
7. When every table has been saved, reply with a short plain-text summary of what you wrote — \
do not call any more tools.

Never invent columns, tables, or relationships that the tools did not return. Ground every claim \
in actual tool output. Where claude.md's conventions (naming, structure, frontmatter, linking) \
conflict with the section list above, follow claude.md.
"""


def build_system_prompt():
    """Fill SYSTEM_PROMPT with claude.md's contents, if any, so the tool-calling agent treats
    the repo's wiki schema/operating rules as binding instructions rather than ignoring them."""
    instructions = load_claude_instructions()
    block = (
        f"The repository defines these wiki conventions in claude.md — treat them as binding "
        f"instructions for how you write and organize wiki content:\n\n{instructions}"
        if instructions
        else "No claude.md was found in the repository; use the section list below as-is."
    )
    return SYSTEM_PROMPT.format(claude_instructions_block=block)


def chat_with_agent(user_instruction, max_rounds=15):
    """Free-form tool-calling chat with the agent (for ad hoc questions). The model decides
    which tools to call and when to stop. Small local models can lose the thread over many
    steps, so prefer run_agent() for reliably generating the full wiki."""
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_instruction},
    ]

    for _ in range(max_rounds):
        response = _client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, max_completion_tokens=800
        )
        msg = response.choices[0].message
        messages.append(msg)

        tool_calls = msg.tool_calls
        if not tool_calls:
            print(msg.content or "")
            return

        for call in tool_calls:
            name = call.function.name
            args = call.function.arguments or {}
            if isinstance(args, str):
                args = json.loads(args)

            print(f"[tool call] {name}({args})")
            impl = TOOL_IMPLS.get(name)
            if impl is None:
                result = {"error": f"unknown tool {name}"}
            else:
                result = impl(**args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, default=str),
                }
            )


COLUMN_DESC_PROMPT = """Table "{table_name}" in a Postgres database has these columns (name, type, \
nullable, default) and these sample rows:

Columns:
{columns_json}

Sample rows:
{sample_json}

For EACH column listed above, write a short (<=15 word) business-meaning description inferred \
from its name, type, and the sample values. Respond with ONLY a JSON object mapping each column \
name to its description string — no other text, no markdown fences.
"""

NARRATIVE_PROMPT = """You are documenting the Postgres table "{table_name}" for a team wiki.

{claude_instructions_block}

Table facts:
- Row count estimate: {row_count}
- Primary key: {primary_key}
- Foreign keys: {foreign_keys}
- Check constraints: {check_constraints}
- Indexes: {indexes}
- Column names and types: {column_names}

Sample rows:
{sample_json}

Write four Markdown sections, in this exact order, headed exactly as shown:

## Overview
(2-4 sentences inferring this table's business purpose from its name, columns, and sample data.)

## Business Rules
(If check_constraints is empty, say plainly that no business rules are enforced at the database \
level, then list 2-5 conventions you observe in the sample data, clearly labeled as *inferred*, \
not enforced. If check_constraints is non-empty, explain each one.)

## Common Query Examples
(2-4 realistic SQL queries against this table using its real column names, each in its own \
```sql``` fenced block with a one-line description above it.)

## Index Documentation
(List the indexes given above with their columns and uniqueness. If there are none, say so, then \
suggest 1-2 indexes that would make sense given the columns and the query examples you just wrote.)

Never invent columns, tables, or relationships not present in the facts above. Follow claude.md's \
conventions (tone, evidence discipline, inference labeling) wherever they apply to these sections. \
Output only the four Markdown sections, nothing else.
"""


REL_NARRATIVE_PROMPT = """You are documenting a foreign-key relationship in a team wiki, between \
Postgres tables "{source_table}" and "{target_table}".

{claude_instructions_block}

Relationship facts (already determined from the live schema — do not second-guess these):
- {source_table}.{source_column} -> {target_table}.{target_column}
- Constraint name: {constraint_name}
- Source column nullable: {source_nullable}
- Cardinality from {source_table} to {target_table}: {cardinality_forward}
- Cardinality from {target_table} to {source_table}: {cardinality_reverse}
- Optionality: each {source_table} row's link to {target_table} is {optionality}
- {source_table} row count estimate: {source_row_count}
- {target_table} row count estimate: {target_row_count}

Sample matched rows (each source row's {source_column} value joined to its {target_table} row):
{samples_json}

Write two Markdown sections, in this exact order, headed exactly as shown:

## Summary
(2-3 sentences: what real-world relationship this foreign key represents, phrased using the exact \
cardinality and optionality facts given above — e.g. "each {target_table} row can have zero or many \
{source_table} rows attached to it; each {source_table} row must belong to exactly one {target_table}." \
Ground the business meaning in the table/column names and the sample matches.)

## Tensions Or Gaps
(1-3 sentences: call out anything that looks like a modeling risk — e.g. an optional FK meaning \
some {source_table} rows may be orphaned by design, or a one-to-one cardinality that might actually \
belong on a single table. If nothing notable, say so plainly rather than inventing an issue.)

Never invent facts not present above, and never restate the cardinality/optionality differently \
than given. Output only the two Markdown sections, nothing else.
"""


DOMAIN_PROMPT = """You are organizing a Postgres schema into business domains for a team wiki, so \
someone can quickly answer "what tables do I need to touch to build feature X" without scanning \
every table.

Tables and their columns:
{tables_json}

Foreign-key relationships (source -> target):
{fks_json}

Group ALL of the tables above into 3-6 business domains (e.g. vendor management, pricing, \
logistics, catalog, performance) — tables that are joined together by foreign keys usually belong \
to the same or a closely related domain. Every table must appear in EXACTLY ONE domain.

Respond with ONLY a JSON object of this exact shape, no other text, no markdown fences:
{{"domains": [{{"name": "Vendor Management", "slug": "vendor-management", "description": "one \
sentence describing what this domain covers", "tables": ["vendors", "vendor_contracts"]}}, ...]}}
"""

QUERY_PROMPT = """You are building a small library of "known good" example SQL queries for a team \
wiki, so an LLM writing new queries against this schema has few-shot examples grounded in the \
real table and column names — never invented ones.

Tables and their columns (with primary/foreign keys noted):
{schema_json}

Required multi-hop join chains: these table pairs have NO direct foreign key between them — the \
only way to connect them is through the intermediate table(s) shown, in this order. A naive query \
writer who only looks at one-to-one relationship docs misses these entirely, so they need their \
own worked examples:
{chains_json}

Write one query for EACH required chain above, joining every table in the chain in the given \
order via the foreign keys implied by the schema above, phrased as the realistic business question \
it answers (e.g. a chain "items -> vendor_pricing -> vendors -> vendor_shipping_points" answers \
"what is the shipping address for a given item"). Then write 5-7 more general canonical business \
queries covering the rest of the schema (mix of single-table and multi-table joins, including \
tables not touched by the chains above). Respond with ONLY a JSON object of this exact shape, no \
other text, no markdown fences:
{{"queries": [{{"title": "Active vendors and their latest price per item", "slug": \
"active-vendors-latest-price", "question": "the business question this answers, as a sentence", \
"sql": "SELECT ... ;", "tables": ["vendors", "vendor_pricing"]}}, ...]}}

Use ONLY table and column names that appear above. Never invent a column or table.
"""


def build_fk_graph(all_fks):
    """Undirected adjacency ({table: {neighbor_table: fk}}) built from every FK's source and \
target side, so chain-finding can walk the graph in either direction."""
    graph = {}
    for fk in all_fks:
        graph.setdefault(fk["source_table"], {})[fk["target_table"]] = fk
        graph.setdefault(fk["target_table"], {})[fk["source_table"]] = fk
    return graph


def _bfs_shortest_paths(graph, start, max_hops):
    """Shortest path (as a list of table names) from `start` to every table reachable within
    max_hops FK-graph edges, keyed by destination table."""
    visited = {start: [start]}
    frontier = [start]
    for _ in range(max_hops):
        next_frontier = []
        for node in frontier:
            for neighbor in graph.get(node, {}):
                if neighbor in visited:
                    continue
                visited[neighbor] = visited[node] + [neighbor]
                next_frontier.append(neighbor)
        frontier = next_frontier
    return visited


def find_sibling_relationships(fk, all_fks):
    """Other FKs that share a table with `fk` (on either side) — e.g. vendor_pricing-items and
    vendor_pricing-vendors both touch vendor_pricing. Linking these directly on a relationship page
    is what turns a 2-hop chain (items -> vendor_pricing -> vendors) into a page-to-page walk a
    navigator can follow without first consulting the full FK graph."""
    tables = {fk["source_table"], fk["target_table"]}
    fk_id = (fk["source_table"], fk["source_column"], fk["target_table"], fk["target_column"])
    siblings = []
    for other in all_fks:
        other_id = (other["source_table"], other["source_column"], other["target_table"], other["target_column"])
        if other_id == fk_id:
            continue
        if other["source_table"] in tables or other["target_table"] in tables:
            siblings.append(other)
    return siblings


def find_multi_hop_chains(all_fks, max_hops=3):
    """Find the shortest join path between every pair of tables that are connected through the FK \
graph but have NO direct FK between them (e.g. items -> vendor_pricing -> vendors -> \
vendor_shipping_points to get a ship address for an item) — exactly the join shape a flat, \
one-relationship-page-at-a-time lookup misses, since no single relationship page documents it. \
Returns a list of paths (each a list of table names), one shortest path per disconnected pair, \
capped at max_hops edges."""
    graph = build_fk_graph(all_fks)
    direct_pairs = {frozenset((fk["source_table"], fk["target_table"])) for fk in all_fks}

    chains = {}  # frozenset(endpoints) -> shortest path found so far
    for start in graph:
        for path in _bfs_shortest_paths(graph, start, max_hops).values():
            if len(path) < 3:
                continue  # need at least one intermediate table to count as "multi-hop"
            endpoints = frozenset((path[0], path[-1]))
            if endpoints in direct_pairs:
                continue  # already covered by a direct relationship page
            if endpoints not in chains or len(path) < len(chains[endpoints]):
                chains[endpoints] = path
    return list(chains.values())


def _chat_json(prompt):
    time.sleep(15)
    try:
        response = _client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_completion_tokens=800,
        )
    except Exception:
        response = _client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=800,
        )
    return json.loads(response.choices[0].message.content)


def _chat_text(prompt):
    time.sleep(15)
    response = _client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}], max_completion_tokens=500
    )
    return response.choices[0].message.content


def get_column_descriptions(table_name, columns, sample_rows, batch_size=20):
    """Ask the model for column descriptions in small batches so it doesn't truncate or drop rows."""
    descriptions = {}
    sample_json = json.dumps(sample_rows[:3], indent=2, default=str)
    for i in range(0, len(columns), batch_size):
        batch = columns[i : i + batch_size]
        prompt = COLUMN_DESC_PROMPT.format(
            table_name=table_name,
            columns_json=json.dumps(batch, indent=2, default=str),
            sample_json=sample_json,
        )
        try:
            descriptions.update(_chat_json(prompt))
        except (json.JSONDecodeError, KeyError):
            for c in batch:
                descriptions.setdefault(c["column_name"], "")
    return descriptions


def render_column_table(columns, descriptions):
    lines = ["| Column | Type | Nullable | Default | Description |", "|---|---|---|---|---|"]
    for c in columns:
        col_type = c["data_type"]
        if c.get("character_maximum_length"):
            col_type += f"({c['character_maximum_length']})"
        elif c.get("numeric_precision") and c["data_type"] == "numeric":
            scale = c.get("numeric_scale") or 0
            col_type += f"({c['numeric_precision']},{scale})"
        nullable = "Yes" if c["is_nullable"] == "YES" else "No"
        default = c["column_default"] or ""
        desc = descriptions.get(c["column_name"], "")
        lines.append(f"| {c['column_name']} | {col_type} | {nullable} | {default} | {desc} |")
    return "\n".join(lines)


def render_migration_history():
    history = db.get_migration_history()
    if not history["table"]:
        return "This database has no migration-tracking table (checked for alembic, flyway, django, knex, and sequelize conventions). Schema changes here are not currently tracked."
    lines = [f"Tracked via `{history['table']}`. Most recent entries:", "", "| " + " | ".join(history["rows"][0].keys()) + " |"]
    lines.append("|" + "---|" * len(history["rows"][0].keys()))
    for row in history["rows"][:20]:
        lines.append("| " + " | ".join(str(v) for v in row.values()) + " |")
    return "\n".join(lines)


def render_erd_section(table_name):
    erd, has_relationships = db.build_erd_for_table(table_name)
    block = f"```mermaid\n{erd}\n```"
    if not has_relationships:
        block += "\n\nThis table has no foreign-key relationships to other tables in the schema."
    return block


NARRATIVE_SECTION_ORDER = ["Overview", "Business Rules", "Common Query Examples", "Index Documentation"]
REL_SECTION_ORDER = ["Summary", "Tensions Or Gaps"]


def parse_narrative_sections(narrative, section_order=NARRATIVE_SECTION_ORDER):
    """Split the model's narrative response into {heading: body} using the '## Heading' markers
    we asked for. Falls back to an empty body for any section the model dropped."""
    pattern = r"##\s*(" + "|".join(re.escape(h) for h in section_order) + r")\s*\n"
    parts = re.split(pattern, narrative)
    sections = dict.fromkeys(section_order, "")
    # re.split with a capturing group yields [pre, heading, body, heading, body, ...]
    for i in range(1, len(parts), 2):
        heading, body = parts[i], parts[i + 1]
        sections[heading] = body.strip()
    return sections


def _pick_descriptive_column(columns):
    """Best-effort pick of a human-readable column (name/desc/title) to show alongside a matched
    target row, so sample tables read as more than a wall of ids."""
    for preferred in ("name", "desc", "title"):
        for c in columns:
            if preferred in c.lower() and c.lower() != "":
                return c
    return columns[0] if columns else None


def render_field_mapping_table(fk):
    return (
        "| Source Field | Target Field |\n"
        "|---|---|\n"
        f"| `{fk['source_table']}.{fk['source_column']}` | `{fk['target_table']}.{fk['target_column']}` |"
    )


def render_sample_matches_table(fk, samples):
    source_col, target_col = fk["source_column"], fk["target_column"]
    target_desc_col = None
    for s in samples:
        if s["target"]:
            target_desc_col = _pick_descriptive_column(list(s["target"].keys()))
            break

    header_cols = [f"{fk['source_table']}.{source_col}", f"{fk['target_table']}.{target_col}"]
    if target_desc_col:
        header_cols.append(f"{fk['target_table']}.{target_desc_col}")
    lines = ["| " + " | ".join(header_cols) + " |", "|" + "---|" * len(header_cols)]

    for s in samples:
        source_val = s["source"].get(source_col)
        if s["target"] is None:
            row = [str(source_val), "*(no matching row — orphaned reference)*"]
            if target_desc_col:
                row.append("")
        else:
            row = [str(source_val), str(s["target"].get(target_col))]
            if target_desc_col:
                row.append(str(s["target"].get(target_desc_col, "")))
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_related_section(related_fks, all_fks, domain_slug=None, enum_columns=None, related_queries=None):
    """Link an entity page out to every relationship page that involves it (as either side of the
    FK), its business domain, any enum-like columns it owns, any canonical query page that touches
    it, and the schema-wide overviews — the cross-linking claude.md requires. The query back-links
    matter for navigation specifically: a query page links forward to the entities it uses, but
    without this, an entity page never links back, so a navigator starting from a table has no way
    to discover which worked examples (including multi-hop join chains) already cover it."""
    lines = [f"- [[relationships/{relationship_filename(fk, all_fks)}]]" for fk in related_fks]
    if related_fks:
        lines.append("- [[relationships/overview]]")
    else:
        lines.append("This table has no foreign-key relationships to other tables in the schema.")
    if domain_slug:
        lines.append(f"- [[domains/{domain_slug}]]")
    for col in enum_columns or []:
        lines.append(f"- [[enums/{col}]]")
    for q in related_queries or []:
        lines.append(f"- [[queries/{q['slug']}]] — {q['title']}")
    lines += ["- [[erd]]", "- [[overview]]", "- [[index]]"]
    return "\n".join(lines) + "\n"


def generate_table_wiki_page(
    table_name, related_fks=None, all_fks=None, domain_slug=None, enum_columns=None,
    corrections=None, related_queries=None,
):
    related_fks = related_fks or []
    all_fks = all_fks or []
    corrections = corrections or {}
    details = db.get_table_details(table_name)
    columns = details["columns"]
    sample_rows = details["sample_rows"]

    descriptions = get_column_descriptions(table_name, columns, sample_rows)
    column_table_md = render_column_table(columns, descriptions)
    erd_section = render_erd_section(table_name)
    migration_section = render_migration_history()

    instructions = load_claude_instructions()
    claude_instructions_block = (
        f"The repository defines these wiki conventions in claude.md — treat them as binding "
        f"instructions for how you write this content:\n\n{instructions}"
        if instructions
        else "No claude.md was found in the repository; use the section instructions below as-is."
    )
    narrative = _chat_text(
        NARRATIVE_PROMPT.format(
            table_name=table_name,
            claude_instructions_block=claude_instructions_block,
            row_count=details["row_count_estimate"],
            primary_key=details["primary_key"] or "none",
            foreign_keys=json.dumps(details["foreign_keys"], default=str) or "none",
            check_constraints=json.dumps(details["check_constraints"], default=str) or "none",
            indexes=json.dumps(details["indexes"], default=str) or "none",
            column_names=[(c["column_name"], c["data_type"]) for c in columns],
            sample_json=json.dumps(sample_rows[:3], indent=2, default=str),
        )
    )
    sections = parse_narrative_sections(narrative)

    gotchas_md = render_corrections_section(corrections.get(table_name, []))
    gotchas_section = f"## Known Query Gotchas\n{gotchas_md}\n\n" if gotchas_md else ""

    content = (
        f"# {table_name}\n\n"
        f"## Overview\n{sections['Overview']}\n\n"
        f"## Entity Relationship Diagram\n{erd_section}\n\n"
        f"## Column Reference Table\n{column_table_md}\n\n"
        f"## Business Rules\n{sections['Business Rules']}\n\n"
        f"## Common Query Examples\n{sections['Common Query Examples']}\n\n"
        f"## Index Documentation\n{sections['Index Documentation']}\n\n"
        f"## Migration History\n{migration_section}\n\n"
        f"{gotchas_section}"
        f"## Related\n{render_related_section(related_fks, all_fks, domain_slug, enum_columns, related_queries)}"
    )

    result = save_wiki_page(table_name, content)
    result["descriptions"] = descriptions
    result["overview_summary"] = _first_sentence(sections["Overview"])
    return result


def save_relationship_page(fk, content, all_fks):
    """Save a finished Markdown relationship page to wiki/relationships/, prefixing claude.md-style
    frontmatter. Preserves the original `created` date across reruns; only `updated` changes."""
    path = os.path.join(RELATIONSHIPS_DIR, f"{relationship_filename(fk, all_fks)}.md")
    existing_fields, _ = _parse_frontmatter(path)
    created = existing_fields.get("created") or date.today().isoformat()
    full_content = render_relationship_frontmatter(fk, created) + content
    with open(path, "w", encoding="utf-8") as f:
        f.write(full_content)
    return {"saved_to": path, "bytes_written": len(full_content.encode("utf-8"))}


def describe_cardinality(fk):
    """Determine the real cardinality/optionality of a FK from schema facts (never guessed by the
    model): a source column that's itself unique/PK makes the relationship one-to-one instead of
    the default many-to-one, and a nullable FK column makes it optional instead of mandatory."""
    is_unique = db.is_column_unique(fk["source_table"], fk["source_column"])
    forward = "one-to-one" if is_unique else "many-to-one"
    reverse = "one-to-one" if is_unique else "one-to-many"
    return {"forward": forward, "reverse": reverse, "source_is_unique": is_unique}


def generate_relationship_page(fk, all_fks, corrections=None):
    """Document one FK relationship: cardinality, optionality, the exact field mapping, and real
    matched sample rows proving the join — so 'relation between each field' is grounded in live
    data rather than left for the model to guess."""
    corrections = corrections or {}
    source_table, source_column = fk["source_table"], fk["source_column"]
    target_table, target_column = fk["target_table"], fk["target_column"]

    source_columns = db.get_columns(source_table)
    source_col_info = next((c for c in source_columns if c["column_name"] == source_column), {})
    source_nullable = source_col_info.get("is_nullable", "unknown")
    optional = source_nullable == "YES"
    cardinality = describe_cardinality(fk)

    samples = db.fetch_relationship_samples(fk)

    instructions = load_claude_instructions()
    claude_instructions_block = (
        f"The repository defines these wiki conventions in claude.md — treat them as binding "
        f"instructions for how you write this content:\n\n{instructions}"
        if instructions
        else "No claude.md was found in the repository; use the section instructions below as-is."
    )
    narrative = _chat_text(
        REL_NARRATIVE_PROMPT.format(
            source_table=source_table,
            target_table=target_table,
            claude_instructions_block=claude_instructions_block,
            source_column=source_column,
            target_column=target_column,
            constraint_name=fk.get("constraint_name", "unknown"),
            source_nullable=source_nullable,
            cardinality_forward=cardinality["forward"],
            cardinality_reverse=cardinality["reverse"],
            optionality="optional (0 or 1)" if optional else "mandatory (exactly 1)",
            source_row_count=db.get_row_count(source_table),
            target_row_count=db.get_row_count(target_table),
            samples_json=json.dumps(samples, indent=2, default=str),
        )
    )
    sections = parse_narrative_sections(narrative, REL_SECTION_ORDER)

    gotchas_md = render_corrections_section(
        corrections.get(source_table, []) + corrections.get(target_table, [])
    )
    gotchas_section = f"## Known Query Gotchas\n{gotchas_md}\n\n" if gotchas_md else ""

    sibling_lines = "".join(
        f"- [[relationships/{relationship_filename(sib, all_fks)}]]\n"
        for sib in find_sibling_relationships(fk, all_fks)
    )

    content = (
        f"# {source_table} → {target_table}\n\n"
        f"## Summary\n{sections['Summary']}\n\n"
        f"## Relationship Definition\n"
        f"| Attribute | Value |\n|---|---|\n"
        f"| Source table | [[entities/{source_table}]] |\n"
        f"| Source column | `{source_column}` |\n"
        f"| Target table | [[entities/{target_table}]] |\n"
        f"| Target column | `{target_column}` |\n"
        f"| Constraint | `{fk.get('constraint_name', 'unknown')}` |\n"
        f"| Cardinality ({source_table} → {target_table}) | {cardinality['forward']} |\n"
        f"| Cardinality ({target_table} → {source_table}) | {cardinality['reverse']} |\n"
        f"| Optionality | {'optional — ' + source_column + ' is nullable' if optional else 'mandatory — ' + source_column + ' is NOT NULL'} |\n\n"
        f"## Field Mapping\n{render_field_mapping_table(fk)}\n\n"
        f"## Sample Matches\n{render_sample_matches_table(fk, samples)}\n\n"
        f"## Tensions Or Gaps\n{sections['Tensions Or Gaps']}\n\n"
        f"{gotchas_section}"
        f"## Related\n"
        f"- [[entities/{source_table}]]\n"
        f"- [[entities/{target_table}]]\n"
        f"{sibling_lines}"
        f"- [[relationships/overview]]\n"
    )

    return save_relationship_page(fk, content, all_fks)


def build_relationships_overview(all_fks):
    """Write wiki/relationships/overview.md: a single table cataloging every FK relationship in
    the schema, linking out to each individual relationship page and both entity pages."""
    today = date.today().isoformat()
    existing_fields, _ = _parse_frontmatter(RELATIONSHIPS_OVERVIEW_PATH)
    created = existing_fields.get("created") or today

    rows = [
        f"| [[entities/{fk['source_table']}]] | `{fk['source_column']}` | [[entities/{fk['target_table']}]] "
        f"| `{fk['target_column']}` | {describe_cardinality(fk)['forward']} "
        f"| [[relationships/{relationship_filename(fk, all_fks)}]] |"
        for fk in sorted(all_fks, key=lambda fk: (fk["source_table"], fk["target_table"]))
    ]

    content = (
        "---\n"
        "title: Schema Relationships Overview\n"
        "type: concept\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        "source_count: 0\n"
        "---\n\n"
        "# Schema Relationships Overview\n\n"
        "## Summary\n"
        f"This page indexes every foreign-key relationship in the live schema ({len(all_fks)} total). "
        "See [[index]] for the full entity catalog and [[overview]] for context.\n\n"
        "## Evidence\n"
        "| Source Table | Source Column | Target Table | Target Column | Cardinality | Detail |\n"
        "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n"
        "## Tensions Or Gaps\n"
        "Each row links to a dedicated relationship page with the field mapping, cardinality, and "
        "real matched sample rows for that FK.\n\n"
        "## Related\n- [[index]]\n- [[overview]]\n"
    )

    with open(RELATIONSHIPS_OVERVIEW_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return RELATIONSHIPS_OVERVIEW_PATH


def generate_domains(tables, all_fks):
    """Single LLM call bucketing every table into a business domain, using columns + FK graph as
    grounding so joined tables tend to land together."""
    tables_json = json.dumps(
        {t: [c["column_name"] for c in db.get_columns(t)] for t in tables}, indent=2
    )
    fks_json = json.dumps(
        [{"source": fk["source_table"], "target": fk["target_table"]} for fk in all_fks], indent=2
    )
    try:
        result = _chat_json(DOMAIN_PROMPT.format(tables_json=tables_json, fks_json=fks_json))
        domains = result.get("domains", [])
    except (json.JSONDecodeError, KeyError):
        domains = []

    # Guard against a small/uncooperative local model: fall back to one catch-all domain so every
    # table still gets a domain page rather than silently having none.
    covered = {t for d in domains for t in d.get("tables", [])}
    missing = [t for t in tables if t not in covered]
    if missing:
        domains.append(
            {
                "name": "Uncategorized",
                "slug": "uncategorized",
                "description": "Tables the domain-grouping step didn't confidently place elsewhere.",
                "tables": missing,
            }
        )
    return domains


def table_domain_map(domains):
    return {t: d["slug"] for d in domains for t in d.get("tables", [])}


def save_domain_page(domain):
    slug = domain["slug"]
    path = os.path.join(DOMAINS_DIR, f"{slug}.md")
    existing_fields, _ = _parse_frontmatter(path)
    created = existing_fields.get("created") or date.today().isoformat()
    today = date.today().isoformat()

    entity_links = "\n".join(f"- [[entities/{t}]]" for t in sorted(domain.get("tables", [])))
    content = (
        "---\n"
        f"title: {domain['name']} Domain\n"
        "type: concept\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        "source_count: 0\n"
        "---\n\n"
        f"# {domain['name']} Domain\n\n"
        f"## Summary\n{domain.get('description', '')}\n\n"
        f"## Evidence\n{entity_links}\n\n"
        "## Tensions Or Gaps\n"
        "Domain grouping is model-inferred from table/column names and FK adjacency; treat it as "
        "*inferred* organization, not an enforced schema boundary.\n\n"
        "## Related\n- [[index]]\n- [[erd]]\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"saved_to": path, "bytes_written": len(content.encode("utf-8"))}


ENUM_NAME_HINTS = ("status", "flag", "type", "code", "indicator", "ind", "group")
ENUM_TEXT_TYPES = {"character varying", "character", "text"}


def detect_enum_candidates(columns):
    """Deterministic heuristic: short/status-shaped text columns are enum candidates. No LLM
    involved here — the goal is to eliminate a source of hallucination, not add one."""
    candidates = []
    for c in columns:
        if c["data_type"] not in ENUM_TEXT_TYPES:
            continue
        name_hits_hint = any(h in c["column_name"].lower() for h in ENUM_NAME_HINTS)
        is_short = (c.get("character_maximum_length") or 999) <= 10
        if name_hits_hint or is_short:
            candidates.append(c["column_name"])
    return candidates


def build_enum_map(tables):
    """Scan every table for enum-candidate columns and pull real distinct values for each. Columns
    with too many distinct values (not actually an enum) are dropped. Returns
    {column_name: {table_name: [{"value":..., "n":...}, ...]}}."""
    enum_map = {}
    for table in tables:
        columns = db.get_columns(table)
        for col in detect_enum_candidates(columns):
            values = db.get_distinct_value_counts(table, col, limit=16)
            if 1 <= len(values) <= 15:
                enum_map.setdefault(col, {})[table] = values
    return enum_map


def save_enum_page(column_name, tables_values):
    path = os.path.join(ENUMS_DIR, f"{column_name}.md")
    existing_fields, _ = _parse_frontmatter(path)
    created = existing_fields.get("created") or date.today().isoformat()
    today = date.today().isoformat()

    sections = []
    for table in sorted(tables_values):
        rows = tables_values[table]
        lines = [f"### `{table}.{column_name}`", "", "| Value | Count |", "|---|---|"]
        lines += [f"| {r['value']} | {r['n']} |" for r in rows]
        sections.append("\n".join(lines))

    distinct_sets = {table: frozenset(str(r["value"]) for r in rows) for table, rows in tables_values.items()}
    drift_note = (
        "All tables using this column name share the same observed value set.\n"
        if len(set(distinct_sets.values())) <= 1
        else "*inferred*: different tables reuse this column name with different observed values — "
        "confirm they mean the same thing before treating them as one shared enum.\n"
    )

    content = (
        "---\n"
        f"title: {column_name} enum\n"
        "type: concept\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        + "".join(f"  - live-database:public.{t}\n" for t in sorted(tables_values))
        + f"source_count: {len(tables_values)}\n"
        "---\n\n"
        f"# {column_name}\n\n"
        f"## Summary\nObserved distinct values for `{column_name}`, queried live from "
        f"{len(tables_values)} table(s) rather than inferred.\n\n"
        f"## Evidence\n{chr(10).join(sections)}\n\n"
        f"## Tensions Or Gaps\n{drift_note}\n"
        "## Related\n"
        + "".join(f"- [[entities/{t}]]\n" for t in sorted(tables_values))
        + "- [[glossary]]\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"saved_to": path, "bytes_written": len(content.encode("utf-8"))}


def generate_queries(tables, all_fks):
    """Single LLM call producing a small few-shot query library grounded in real table/column
    names and the FK graph, saved as claude.md-shaped analysis pages."""
    schema = {
        t: {
            "columns": [c["column_name"] for c in db.get_columns(t)],
            "primary_key": [r["column_name"] for r in db.get_primary_keys(t)],
        }
        for t in tables
    }
    schema["_foreign_keys"] = [
        f"{fk['source_table']}.{fk['source_column']} -> {fk['target_table']}.{fk['target_column']}"
        for fk in all_fks
    ]
    chains = find_multi_hop_chains(all_fks)
    chains_json = json.dumps([" -> ".join(c) for c in chains], indent=2) if chains else "(none found)"
    try:
        result = _chat_json(
            QUERY_PROMPT.format(schema_json=json.dumps(schema, indent=2), chains_json=chains_json)
        )
        return result.get("queries", [])
    except (json.JSONDecodeError, KeyError):
        return []


def save_query_page(query):
    slug = query.get("slug") or re.sub(r"[^a-z0-9]+", "-", query.get("title", "query").lower()).strip("-")
    path = os.path.join(QUERIES_DIR, f"{slug}.md")
    existing_fields, _ = _parse_frontmatter(path)
    created = existing_fields.get("created") or date.today().isoformat()
    today = date.today().isoformat()

    table_links = "\n".join(f"- [[entities/{t}]]" for t in query.get("tables", []))
    content = (
        "---\n"
        f"title: {query.get('title', slug)}\n"
        "type: analysis\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        "source_count: 0\n"
        "---\n\n"
        f"# {query.get('title', slug)}\n\n"
        f"## Prompt\n{query.get('question', '')}\n\n"
        f"## Conclusion\nCanonical query grounded in the current live schema — see [[erd]] for the "
        "full relationship context.\n\n"
        f"## Evidence\n```sql\n{query.get('sql', '')}\n```\n\nTables involved:\n{table_links}\n\n"
        "## Follow-ups\nNone noted.\n\n"
        "## Related\n- [[index]]\n- [[glossary]]\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"saved_to": path, "bytes_written": len(content.encode("utf-8"))}, slug


def build_glossary(all_descriptions):
    """Aggregate the column descriptions already generated per entity page into one cross-table
    glossary, so business language maps to schema language in a single place."""
    existing_fields, _ = _parse_frontmatter(GLOSSARY_PATH)
    created = existing_fields.get("created") or date.today().isoformat()
    today = date.today().isoformat()

    by_column = {}
    for table, descriptions in all_descriptions.items():
        for column, desc in descriptions.items():
            by_column.setdefault(column, {})[table] = desc

    rows = []
    for column in sorted(by_column):
        table_entries = by_column[column]
        table_links = ", ".join(f"[[entities/{t}]]" for t in sorted(table_entries))
        description = next(iter(table_entries.values()), "")
        rows.append(f"| `{column}` | {table_links} | {description} |")

    content = (
        "---\n"
        "title: Glossary\n"
        "type: concept\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        "source_count: 0\n"
        "---\n\n"
        "# Glossary\n\n"
        "## Summary\n"
        f"Business terms mapped to their schema representation, aggregated from column "
        f"descriptions across all {len(all_descriptions)} entity pages.\n\n"
        "## Evidence\n"
        "| Column | Tables | Description |\n|---|---|---|\n" + "\n".join(rows) + "\n\n"
        "## Tensions Or Gaps\n"
        "Where a column name is reused across tables, the description shown is from its first "
        "occurrence; wording may vary slightly per table — see the individual entity page for the "
        "exact text. See [[enums]] pages for columns whose valid values are also documented.\n\n"
        "## Related\n- [[index]]\n- [[conventions]]\n"
    )
    with open(GLOSSARY_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return GLOSSARY_PATH


AUDIT_PAIR_NAMES = [("created_timestamp", "updated_timestamp"), ("created_at", "updated_at")]
SOFT_DELETE_HINTS = ("is_deleted", "deleted_at", "deleted", "active_flag", "inactive")


def scan_conventions(tables):
    """Deterministic pattern scan across every table's real columns — no LLM guessing, everything
    here is a fact observed directly from information_schema."""
    audit_tables, soft_delete_hits, flag_char1_hits, pk_patterns = [], [], [], []
    timestamp_type_counts = {}

    for table in tables:
        columns = db.get_columns(table)
        names = {c["column_name"] for c in columns}
        if any(set(pair) <= names for pair in AUDIT_PAIR_NAMES):
            audit_tables.append(table)
        for c in columns:
            col = c["column_name"]
            if col in SOFT_DELETE_HINTS:
                soft_delete_hits.append(f"{table}.{col}")
            if c["data_type"] == "character" and (c.get("character_maximum_length") or 0) == 1:
                flag_char1_hits.append(f"{table}.{col}")
            if "timestamp" in c["data_type"]:
                timestamp_type_counts[c["data_type"]] = timestamp_type_counts.get(c["data_type"], 0) + 1

        pk_cols = [r["column_name"] for r in db.get_primary_keys(table)]
        if len(pk_cols) == 1:
            pk_patterns.append(f"{table}: `{pk_cols[0]}`" + (" (matches `<table>_id`)" if pk_cols[0].startswith(table.rstrip("s")[:4]) else ""))
        elif pk_cols:
            pk_patterns.append(f"{table}: composite (`{', '.join(pk_cols)}`)")

    return {
        "audit_tables": audit_tables,
        "soft_delete_hits": soft_delete_hits,
        "flag_char1_hits": flag_char1_hits,
        "timestamp_type_counts": timestamp_type_counts,
        "pk_patterns": pk_patterns,
    }


def build_conventions(tables):
    existing_fields, _ = _parse_frontmatter(CONVENTIONS_PATH)
    created = existing_fields.get("created") or date.today().isoformat()
    today = date.today().isoformat()
    facts = scan_conventions(tables)

    audit_line = (
        f"*inferred*: {len(facts['audit_tables'])}/{len(tables)} table(s) follow a "
        f"`created_timestamp`/`updated_timestamp` (or `created_at`/`updated_at`) audit-column pair: "
        f"{', '.join(f'`{t}`' for t in facts['audit_tables']) or 'none'}."
    )
    soft_delete_line = (
        f"*inferred*: soft-delete/active-flag style columns found on: "
        f"{', '.join(f'`{c}`' for c in facts['soft_delete_hits']) or 'none observed'}."
    )
    flag_line = (
        f"*inferred*: single-character (`CHAR(1)`) flag columns, likely Y/N-style booleans: "
        f"{', '.join(f'`{c}`' for c in facts['flag_char1_hits']) or 'none observed'}."
    )
    ts_line = (
        "*inferred*: timestamp column types in use — "
        + (", ".join(f"`{k}` ({v} column(s))" for k, v in facts["timestamp_type_counts"].items()) or "none")
        + ". None of these are timezone-aware (`timestamp with time zone`); treat all timestamps as naive/local unless a source says otherwise."
    )
    pk_lines = "\n".join(f"- {line}" for line in facts["pk_patterns"])

    content = (
        "---\n"
        "title: Conventions\n"
        "type: concept\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        "source_count: 0\n"
        "---\n\n"
        "# Conventions\n\n"
        "## Summary\n"
        "Naming, audit-column, soft-delete, and timestamp patterns observed across the live schema. "
        "This consolidates what would otherwise be repeated on every entity page.\n\n"
        "## Evidence\n"
        f"- {audit_line}\n- {soft_delete_line}\n- {flag_line}\n- {ts_line}\n\n"
        f"### Primary key naming per table\n{pk_lines}\n\n"
        "## Tensions Or Gaps\n"
        "All patterns on this page are *inferred* from observed column names/types, not enforced by "
        "the database — treat them as convention, not guarantee.\n\n"
        "## Related\n- [[index]]\n- [[glossary]]\n- [[erd]]\n"
    )
    with open(CONVENTIONS_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return CONVENTIONS_PATH


def build_erd_page(tables, all_fks):
    existing_fields, _ = _parse_frontmatter(ERD_PATH)
    created = existing_fields.get("created") or date.today().isoformat()
    today = date.today().isoformat()
    mermaid = db.build_erd_mermaid()

    content = (
        "---\n"
        "title: Full Schema ERD\n"
        "type: concept\n"
        "status: active\n"
        f"created: {created}\n"
        f"updated: {today}\n"
        "source_paths:\n"
        "source_count: 0\n"
        "---\n\n"
        "# Full Schema ERD\n\n"
        "## Summary\n"
        f"Full entity-relationship diagram for all {len(tables)} tables and {len(all_fks)} "
        "foreign-key relationships in the live schema — a single-glance mental model before "
        "diving into individual entity pages.\n\n"
        f"## Evidence\n```mermaid\n{mermaid}\n```\n\n"
        "## Related\n- [[index]]\n- [[relationships/overview]]\n"
    )
    with open(ERD_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return ERD_PATH


def _migrate_legacy_flat_pages(tables):
    """One-time cleanup: earlier runs wrote wiki/<table>.md directly instead of wiki/entities/.
    Remove those now-superseded flat files so they don't linger as orphans next to entities/."""
    for table in tables:
        legacy_path = os.path.join(WIKI_DIR, f"{table}.md")
        if os.path.isfile(legacy_path):
            os.remove(legacy_path)
            print(f"[cleanup] removed legacy {legacy_path}")


def _prune_stale_pages(directory, keep_filenames):
    """Remove .md files left over from a previous run that no longer appear in this run's output.
    Needed for domains/ and queries/ specifically: their filenames come from LLM-chosen slugs that
    can shift between runs (unlike entity/relationship/enum filenames, which are schema-derived and
    stable), so a stale page could otherwise linger and dangle-link from the index."""
    if not os.path.isdir(directory):
        return
    for filename in os.listdir(directory):
        if filename.endswith(".md") and filename not in keep_filenames:
            os.remove(os.path.join(directory, filename))
            print(f"[cleanup] removed stale {os.path.join(directory, filename)}")


def build_query_table_map(saved_queries):
    """{table_name: [{'slug':..., 'title':...}, ...]} — which canonical query pages touch each
    table, so entity pages can link forward to the worked examples that already cover them."""
    query_map = {}
    for q in saved_queries:
        for table in q.get("tables", []):
            query_map.setdefault(table, []).append({"slug": q["slug"], "title": q["title"]})
    return query_map


def _generate_entity_pages(tables, all_fks, domain_map, enum_map, corrections=None, query_map=None):
    query_map = query_map or {}
    saved_paths, all_descriptions, table_summaries = [], {}, {}
    for table in tables:
        related_fks = [fk for fk in all_fks if table in (fk["source_table"], fk["target_table"])]
        enum_columns = [col for col, by_table in enum_map.items() if table in by_table]
        print(f"[entity] {table}")
        result = generate_table_wiki_page(
            table,
            related_fks=related_fks,
            all_fks=all_fks,
            domain_slug=domain_map.get(table),
            enum_columns=enum_columns,
            corrections=corrections,
            related_queries=query_map.get(table, []),
        )
        saved_paths.append(result["saved_to"])
        all_descriptions[table] = result["descriptions"]
        table_summaries[table] = result["overview_summary"]
        print(f"  saved -> {result['saved_to']} ({result['bytes_written']} bytes)")
    return saved_paths, all_descriptions, table_summaries


def _generate_relationship_pages(all_fks, corrections=None):
    paths = []
    for fk in all_fks:
        print(f"[relationship] {fk['source_table']}.{fk['source_column']} -> {fk['target_table']}.{fk['target_column']}")
        result = generate_relationship_page(fk, all_fks, corrections=corrections)
        paths.append(result["saved_to"])
        print(f"  saved -> {result['saved_to']} ({result['bytes_written']} bytes)")
    paths.append(build_relationships_overview(all_fks))
    return paths


def _generate_domain_pages(domains):
    paths = []
    for domain in domains:
        result = save_domain_page(domain)
        paths.append(result["saved_to"])
        print(f"[domain] {domain['name']} -> {result['saved_to']}")
    return paths


def _generate_enum_pages(enum_map):
    paths = []
    for column, by_table in enum_map.items():
        result = save_enum_page(column, by_table)
        paths.append(result["saved_to"])
        print(f"[enum] {column} ({len(by_table)} table(s)) -> {result['saved_to']}")
    return paths


def _generate_query_pages(tables, all_fks):
    schema_columns = db.get_schema_columns(tables)
    queries = generate_queries(tables, all_fks)

    paths, saved_queries = [], []
    for query in queries:
        is_valid, reason = db.validate_query_sql(query.get("sql", ""), schema_columns)
        if not is_valid:
            print(f"[query] DROPPED '{query.get('title', '?')}': {reason}")
            continue
        result, slug = save_query_page(query)
        paths.append(result["saved_to"])
        saved_queries.append({"slug": slug, "title": query.get("title", slug), "tables": query.get("tables", [])})
        print(f"[query] {slug} -> {result['saved_to']}")
    return paths, saved_queries


def run_agent():
    """Deterministically walk every table, fetch its real schema data straight from Postgres, and
    use the local model only to write grounded narrative sections. Facts (types, nullability, FKs,
    cardinality, enum values, indexes, migration history) are rendered directly from the database,
    never left to the model to transcribe. Builds the full wiki/ layout claude.md + this project's
    schema call for: entities/, relationships/, domains/, enums/, queries/, glossary.md,
    conventions.md, erd.md, plus index.md and log.md."""
    ensure_scaffold()
    tables = db.list_tables()
    _migrate_legacy_flat_pages(tables)
    all_fks = db.get_foreign_keys()

    print("[enums] scanning for enum-like columns...")
    enum_map = build_enum_map(tables)

    print("[domains] grouping tables into business domains...")
    domains = generate_domains(tables, all_fks)
    domain_map = table_domain_map(domains)

    corrections = load_corrections()
    if corrections:
        print(f"[corrections] found {sum(len(v) for v in corrections.values())} logged sql_query_agent "
              f"failure(s) across {len(corrections)} table(s); folding into affected pages")

    # Queries must be generated before entities: entity pages link forward to the canonical query
    # pages that touch them, so the query -> table map needs to exist first.
    query_paths, saved_queries = _generate_query_pages(tables, all_fks)
    _prune_stale_pages(QUERIES_DIR, {f"{q['slug']}.md" for q in saved_queries})
    query_map = build_query_table_map(saved_queries)

    entity_paths, all_descriptions, table_summaries = _generate_entity_pages(
        tables, all_fks, domain_map, enum_map, corrections=corrections, query_map=query_map
    )
    relationship_paths = _generate_relationship_pages(all_fks, corrections=corrections)

    domain_paths = _generate_domain_pages(domains)
    _prune_stale_pages(DOMAINS_DIR, {f"{d['slug']}.md" for d in domains})

    enum_paths = _generate_enum_pages(enum_map)

    glossary_path = build_glossary(all_descriptions)
    conventions_path = build_conventions(tables)
    erd_path = build_erd_page(tables, all_fks)
    print(f"[glossary] updated -> {glossary_path}")
    print(f"[conventions] updated -> {conventions_path}")
    print(f"[erd] updated -> {erd_path}")

    update_index(
        tables,
        all_fks,
        domains=domains,
        enum_columns=list(enum_map.keys()),
        queries=saved_queries,
        table_summaries=table_summaries,
    )

    all_paths = (
        entity_paths + relationship_paths + domain_paths + enum_paths + query_paths
        + [glossary_path, conventions_path, erd_path, INDEX_PATH]
    )
    corrections_note = ""
    if corrections:
        n_entries = sum(len(v) for v in corrections.values())
        corrections_note = (
            f" Folded in {n_entries} sql_query_agent correction(s) logged against "
            f"{', '.join(sorted(corrections))} as 'Known Query Gotchas' sections, then archived "
            f"them to wiki/corrections_archive.md."
        )
        archive_corrections()
        print(f"[corrections] archived -> {CORRECTIONS_ARCHIVE_PATH}")

    append_log_entry(
        operation="ingest",
        title="Regenerate full wiki from live schema",
        paths=["wiki/"] + [os.path.relpath(p, os.path.dirname(__file__)) for p in all_paths],
        summary=(
            f"wiki_agent.py regenerated {len(tables)} entity page(s), {len(all_fks)} relationship "
            f"page(s), {len(domains)} domain page(s), {len(enum_map)} enum page(s), and "
            f"{len(saved_queries)} canonical query page(s) from the live Postgres schema; rebuilt "
            f"glossary.md, conventions.md, erd.md, and index.md.{corrections_note}"
        ),
    )
    print(f"[index] updated -> {INDEX_PATH}")
    print(f"[log] appended -> {LOG_PATH}")


if __name__ == "__main__":
    run_agent()
