import re

from psycopg2.extras import RealDictCursor

from dbconnection import get_connection

MIGRATION_TABLE_CANDIDATES = [
    "alembic_version",
    "schema_migrations",
    "flyway_schema_history",
    "django_migrations",
    "knex_migrations",
    "sequelize_meta",
]


def _query(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def list_tables():
    """List all tables in the public schema."""
    rows = _query(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """
    )
    return [r["table_name"] for r in rows]


def get_columns(table_name):
    """Column reference data: name, type, nullability, default, and comment for a table."""
    columns = _query(
        """
        SELECT
            c.column_name,
            c.data_type,
            c.character_maximum_length,
            c.numeric_precision,
            c.numeric_scale,
            c.is_nullable,
            c.column_default,
            pgd.description AS column_comment
        FROM information_schema.columns c
        LEFT JOIN pg_catalog.pg_statio_all_tables st
            ON st.schemaname = c.table_schema AND st.relname = c.table_name
        LEFT JOIN pg_catalog.pg_description pgd
            ON pgd.objoid = st.relid AND pgd.objsubid = c.ordinal_position
        WHERE c.table_schema = 'public' AND c.table_name = %s
        ORDER BY c.ordinal_position;
        """,
        (table_name,),
    )
    return columns


def get_primary_keys(table_name):
    """Primary key columns for a table."""
    return _query(
        """
        SELECT kcu.column_name
        FROM information_schema.table_constraints tco
        JOIN information_schema.key_column_usage kcu
            ON kcu.constraint_name = tco.constraint_name
            AND kcu.constraint_schema = tco.constraint_schema
        WHERE tco.table_schema = 'public'
            AND tco.table_name = %s
            AND tco.constraint_type = 'PRIMARY KEY'
        ORDER BY kcu.ordinal_position;
        """,
        (table_name,),
    )


def get_foreign_keys(table_name=None):
    """Foreign key relationships (optionally filtered to one table) — used to build the ERD."""
    sql = """
        SELECT
            tc.table_name AS source_table,
            kcu.column_name AS source_column,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column,
            tc.constraint_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON kcu.constraint_name = tc.constraint_name
            AND kcu.constraint_schema = tc.constraint_schema
        JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.constraint_schema = tc.constraint_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public'
    """
    params = ()
    if table_name:
        sql += " AND tc.table_name = %s"
        params = (table_name,)
    sql += " ORDER BY tc.table_name;"
    return _query(sql, params)


def get_indexes(table_name):
    """Index documentation: index name, columns, and uniqueness for a table."""
    return _query(
        """
        SELECT
            i.relname AS index_name,
            a.attname AS column_name,
            ix.indisunique AS is_unique,
            ix.indisprimary AS is_primary
        FROM pg_class t
        JOIN pg_index ix ON t.oid = ix.indrelid
        JOIN pg_class i ON i.oid = ix.indexrelid
        JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
        JOIN pg_namespace n ON n.oid = t.relnamespace
        WHERE n.nspname = 'public' AND t.relname = %s
        ORDER BY i.relname;
        """,
        (table_name,),
    )


def get_check_constraints(table_name):
    """CHECK constraints on a table — the closest thing Postgres has to enforced business rules."""
    return _query(
        """
        SELECT tc.constraint_name, cc.check_clause
        FROM information_schema.table_constraints tc
        JOIN information_schema.check_constraints cc
            ON cc.constraint_name = tc.constraint_name
            AND cc.constraint_schema = tc.constraint_schema
        WHERE tc.table_schema = 'public'
            AND tc.table_name = %s
            AND tc.constraint_type = 'CHECK';
        """,
        (table_name,),
    )


def get_table_comment(table_name):
    """The table-level COMMENT, if one has been set."""
    rows = _query(
        """
        SELECT obj_description(c.oid) AS comment
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public' AND c.relname = %s;
        """,
        (table_name,),
    )
    return rows[0]["comment"] if rows else None

def get_row_count(table_name):
    """Approximate row count for a table (from planner statistics)."""
    rows = _query(
        """
        SELECT reltuples::bigint AS estimate
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public' AND c.relname = %s;
        """,
        (table_name,),
    )
    return rows[0]["estimate"] if rows else None


def get_sample_rows(table_name, limit=5):
    """A small sample of real rows, so the LLM can ground business rules and query examples in actual data."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f'SELECT * FROM "{table_name}" LIMIT %s;', (limit,))
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def get_migration_history():
    """Look for a known migration-tracking table (alembic, flyway, django, knex, sequelize) and return its rows."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for candidate in MIGRATION_TABLE_CANDIDATES:
                cur.execute("SELECT to_regclass(%s) AS exists;", (f"public.{candidate}",))
                if cur.fetchone()["exists"]:
                    cur.execute(f'SELECT * FROM "{candidate}" ORDER BY 1 DESC LIMIT 50;')
                    return {"table": candidate, "rows": [dict(r) for r in cur.fetchall()]}
            return {"table": None, "rows": []}
    finally:
        conn.close()


def get_table_details(table_name):
    """Everything needed to document one table in a single call: columns, PK, FKs, indexes, checks, comment, row count, sample rows."""
    return {
        "table_name": table_name,
        "comment": get_table_comment(table_name),
        "row_count_estimate": get_row_count(table_name),
        "columns": get_columns(table_name),
        "primary_key": [r["column_name"] for r in get_primary_keys(table_name)],
        "foreign_keys": get_foreign_keys(table_name),
        "indexes": get_indexes(table_name),
        "check_constraints": get_check_constraints(table_name),
        "sample_rows": get_sample_rows(table_name),
    }


def get_distinct_value_counts(table_name, column_name, limit=20):
    """Distinct values + row counts for one column. Used to detect enum/status/flag-like columns
    deterministically from real data, rather than asking the model to guess at valid values."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                f'SELECT "{column_name}" AS value, count(*) AS n FROM "{table_name}" '
                f'GROUP BY "{column_name}" ORDER BY n DESC LIMIT %s;',
                (limit,),
            )
            return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def is_column_unique(table_name, column_name):
    """True if column_name is the sole primary key column, or has a single-column unique index —
    the signal used to tell a many-to-one FK apart from a one-to-one FK."""
    pk_cols = {r["column_name"] for r in get_primary_keys(table_name)}
    if pk_cols == {column_name}:
        return True

    indexes = get_indexes(table_name)
    cols_by_index = {}
    unique_by_index = {}
    for row in indexes:
        cols_by_index.setdefault(row["index_name"], []).append(row["column_name"])
        unique_by_index[row["index_name"]] = row["is_unique"]
    return any(
        unique_by_index.get(name) and cols == [column_name]
        for name, cols in cols_by_index.items()
    )


def get_schema_columns(tables=None):
    """{table_name: set(column_names)} for the given tables (or every table if omitted). Shared
    ground-truth used to validate any LLM-generated SQL before it's published or executed."""
    tables = tables if tables is not None else list_tables()
    return {t: {c["column_name"] for c in get_columns(t)} for t in tables}


def _extract_table_aliases(sql, known_tables):
    """Map both real table names and any 'FROM/JOIN table [AS] alias' aliases used in the SQL
    back to the real table name, so column references through an alias can still be checked."""
    aliases = {t: t for t in known_tables}
    for m in re.finditer(r"\b(?:FROM|JOIN)\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?", sql, re.IGNORECASE):
        table, alias = m.group(1), m.group(2)
        if table not in known_tables:
            continue
        if alias and alias.upper() not in ("ON", "WHERE", "GROUP", "ORDER", "JOIN", "AS"):
            aliases[alias] = table
    return aliases


def _extract_cte_names(sql):
    """Names declared via 'WITH x AS (' or ', y AS (' — these are query-local, not real tables,
    and must be excluded from the FROM/JOIN table-existence check below."""
    return set(re.findall(r"(\w+)\s+AS\s*\(", sql, re.IGNORECASE))


SQL_RESERVED_WORDS = {
    "select", "from", "where", "and", "or", "not", "null", "is", "in", "like", "ilike", "between",
    "order", "by", "group", "having", "limit", "offset", "as", "on", "join", "left", "right",
    "inner", "outer", "full", "cross", "distinct", "case", "when", "then", "else", "end",
    "asc", "desc", "with", "union", "all", "exists", "cast", "true", "false", "interval",
    "extract", "now", "count", "sum", "avg", "min", "max", "coalesce", "over", "partition",
    "into", "values", "returning", "using", "date", "timestamp", "numeric", "text", "integer",
}


def _strip_string_literals(sql):
    """Blank out '...'-quoted string literals (Postgres escapes an embedded quote as ''), so a
    literal value like 'V00999' is never mistaken for a column identifier."""
    return re.sub(r"'(?:[^']|'')*'", "''", sql)


def _extract_select_where_identifiers(sql):
    """Bare (unqualified) identifiers referenced in the SELECT list or WHERE clause, excluding SQL
    reserved words, function-call names (an identifier immediately followed by '(' ), and anything
    inside a string literal. Only meaningful for a single flat SELECT — callers are responsible for
    not invoking this on a query containing a CTE or subquery, where "the" FROM/SELECT to scan is
    ambiguous."""
    sql = _strip_string_literals(sql)
    match = re.search(
        r"select\s+(.*?)\s+from\b(.*?)(?:\bgroup\s+by\b|\border\s+by\b|\blimit\b|;|$)",
        sql, re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return set()
    text = match.group(1) + " " + match.group(2)
    identifiers = set()
    for m in re.finditer(r"\b([a-zA-Z_]\w*)\b(\s*\()?", text):
        name, is_call = m.group(1), m.group(2)
        if is_call or name.lower() in SQL_RESERVED_WORDS:
            continue
        identifiers.add(name)
    return identifiers


_FUNC_FROM_RE = re.compile(r"\b(?:EXTRACT|SUBSTRING|TRIM|OVERLAY)\s*\([^()]*?\bFROM\b", re.IGNORECASE)


def _mask_function_from_keyword(sql):
    """Blank out the FROM keyword inside EXTRACT(field FROM expr)-style function calls before
    scanning for FROM/JOIN clause table names — that FROM is function syntax, not a table
    reference, but a plain regex table scan can't otherwise tell the difference. Without this,
    'EXTRACT(YEAR FROM po.po_date)' gets misread as 'FROM po', wrongly flagging a perfectly valid
    alias as a nonexistent table and derailing self-correction down the wrong path (it was blamed
    for a table/alias problem that never existed, instead of the real missing-column problem)."""
    return _FUNC_FROM_RE.sub(lambda m: re.sub(r"\bFROM\b", "XFROM", m.group(0), flags=re.IGNORECASE), sql)


def _check_from_join_tables(sql, known_tables, cte_names):
    """Return (from_tables, error) — error is a (False, reason) tuple if a FROM/JOIN target isn't a
    real table or CTE name; from_tables lists only the real-table targets found."""
    from_tables = []
    for m in re.finditer(r"\b(?:FROM|JOIN)\s+(\w+)", _mask_function_from_keyword(sql), re.IGNORECASE):
        table = m.group(1)
        if table in cte_names:
            continue
        if table not in known_tables:
            return from_tables, (False, f"table `{table}` referenced in FROM/JOIN does not exist in the schema")
        from_tables.append(table)
    return from_tables, None


def _check_qualified_columns(sql, schema_columns):
    """Error tuple if any '<table_or_alias>.<column>' reference doesn't exist on its table."""
    aliases = _extract_table_aliases(sql, schema_columns.keys())
    for prefix, column in re.findall(r"\b(\w+)\.(\w+)\b", sql):
        table = aliases.get(prefix)
        if table is None:
            continue  # not a recognized table/alias prefix — leave unqualified refs unchecked
        if column not in schema_columns[table]:
            return False, f"{prefix}.{column} does not exist on table `{table}`"
    return None


def _check_unqualified_columns(sql, schema_columns, from_tables):
    """For the simple single-table, single-SELECT, no-join, no-CTE shape, error tuple if any bare
    SELECT/WHERE identifier doesn't exist on that one table — catches a hallucinated unqualified
    column (e.g. inventing 'vendor_storage_type' on 'source_vendors') that the qualified-reference
    check can't see, since it never carries a table prefix to check against. Deliberately bails out
    on anything with a CTE or a subquery (more than one SELECT), where "the" table to check an
    unqualified identifier against is ambiguous and a naive scan produces false positives."""
    join_count = len(re.findall(r"\bJOIN\b", sql, re.IGNORECASE))
    select_count = len(re.findall(r"\bSELECT\b", sql, re.IGNORECASE))
    has_cte = bool(re.search(r"\bWITH\b", sql, re.IGNORECASE))
    if len(from_tables) != 1 or join_count != 0 or select_count != 1 or has_cte:
        return None
    table = from_tables[0]
    known_tables = set(schema_columns.keys())
    for ident in _extract_select_where_identifiers(sql):
        if ident in known_tables or ident in schema_columns[table]:
            continue
        return False, f"{ident} does not exist on table `{table}`"
    return None


def validate_query_sql(sql, schema_columns):
    """Check that every FROM/JOIN target names a real table, that every '<table_or_alias>.<column>'
    reference exists on the real schema, and — for the common single-table-no-join shape — that
    every bare column named in the SELECT list or WHERE clause exists on that table. Catches both a
    fully invented table and the model leaking/inventing a column, so a hallucinated query can be
    caught before it's published or run, rather than failing at the database with a confusing error."""
    known_tables = set(schema_columns.keys())
    cte_names = _extract_cte_names(sql)

    from_tables, error = _check_from_join_tables(sql, known_tables, cte_names)
    if error:
        return error

    error = _check_qualified_columns(sql, schema_columns)
    if error:
        return error

    error = _check_unqualified_columns(sql, schema_columns, from_tables)
    if error:
        return error

    return True, None


def fetch_relationship_samples(fk, limit=5):
    """For one FK relationship, pull real source rows plus the target row each one actually
    points to, so relationship pages can show a concrete field-to-field join instead of just
    describing it abstractly."""
    source_table, source_column = fk["source_table"], fk["source_column"]
    target_table, target_column = fk["target_table"], fk["target_column"]
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                f'SELECT * FROM "{source_table}" WHERE "{source_column}" IS NOT NULL LIMIT %s;',
                (limit,),
            )
            source_rows = [dict(r) for r in cur.fetchall()]

            samples = []
            for row in source_rows:
                value = row.get(source_column)
                cur.execute(
                    f'SELECT * FROM "{target_table}" WHERE "{target_column}" = %s LIMIT 1;',
                    (value,),
                )
                target_row = cur.fetchone()
                samples.append({"source": row, "target": dict(target_row) if target_row else None})
            return samples
    finally:
        conn.close()


def build_erd_mermaid():
    """Build a Mermaid erDiagram for every table + FK relationship in the schema (deterministic, not LLM-generated)."""
    tables = list_tables()
    all_fks = get_foreign_keys()
    lines = ["erDiagram"]
    for t in tables:
        cols = get_columns(t)
        pk_cols = {r["column_name"] for r in get_primary_keys(t)}
        lines.append(f"    {t} {{")
        for c in cols:
            key_marker = "PK" if c["column_name"] in pk_cols else ""
            safe_type = c["data_type"].replace(" ", "_")
            lines.append(f'        {safe_type} {c["column_name"]} {key_marker}'.rstrip())
        lines.append("    }")
    for fk in all_fks:
        lines.append(
            f'    {fk["source_table"]} }}o--|| {fk["target_table"]} : "{fk["source_column"]} -> {fk["target_column"]}"'
        )
    return "\n".join(lines)


def build_erd_for_table(table_name):
    """Build a Mermaid erDiagram limited to one table and any tables it has FK relationships with."""
    related_fks = get_foreign_keys(table_name)
    related_tables = {table_name} | {fk["target_table"] for fk in related_fks}

    all_fks = get_foreign_keys()
    incoming_fks = [fk for fk in all_fks if fk["target_table"] == table_name]
    related_tables |= {fk["source_table"] for fk in incoming_fks}

    lines = ["erDiagram"]
    for t in sorted(related_tables):
        cols = get_columns(t)
        pk_cols = {r["column_name"] for r in get_primary_keys(t)}
        lines.append(f"    {t} {{")
        for c in cols:
            key_marker = "PK" if c["column_name"] in pk_cols else ""
            safe_type = c["data_type"].replace(" ", "_")
            lines.append(f'        {safe_type} {c["column_name"]} {key_marker}'.rstrip())
        lines.append("    }")
    for fk in related_fks + incoming_fks:
        lines.append(
            f'    {fk["source_table"]} }}o--|| {fk["target_table"]} : "{fk["source_column"]} -> {fk["target_column"]}"'
        )
    return "\n".join(lines), bool(related_fks or incoming_fks)
