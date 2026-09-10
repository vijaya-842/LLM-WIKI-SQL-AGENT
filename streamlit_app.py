"""Sample Streamlit UI for the wiki-grounded NL-to-SQL agent.

Run with: streamlit run streamlit_app.py
"""

import pandas as pd
import streamlit as st

from sql_query_agent import (
    MODEL,
    generate_sql,
    load_entity_docs,
    load_wiki_page,
    run_sql,
)

st.set_page_config(page_title="Wiki SQL Agent", page_icon="🗄️", layout="centered")

st.title("🗄️ Wiki SQL Agent")
st.caption(f"Ask a question in plain English — SQL is generated from the data wiki using `{MODEL}` via Ollama.")

docs = load_entity_docs()

if not docs:
    st.error("No wiki pages found in the `wiki/` folder. Run `wiki_agent.py` first to generate them.")
    st.stop()

with st.sidebar:
    st.subheader("Tables in the wiki")
    for table_name in sorted(docs):
        st.markdown(f"- `{table_name}`")

question = st.text_input(
    "Your question",
    placeholder="e.g. Show the 5 most recent growth opportunity events at PHOENIX",
)

col1, col2 = st.columns([1, 1])
generate_clicked = col1.button("Generate SQL", type="primary", use_container_width=True)
auto_run = col2.checkbox("Run automatically", value=True)

if "sql" not in st.session_state:
    st.session_state.sql = ""
    st.session_state.pages_used = []
    st.session_state.navigation_reasoning = ""
    st.session_state.sql_explanation = ""
    st.session_state.corrected = False

if generate_clicked:
    if not question.strip():
        st.warning("Type a question first.")
    else:
        with st.spinner("Generating SQL..."):
            try:
                result = generate_sql(question)
                st.session_state.sql = result["sql"]
                st.session_state.pages_used = result["pages_used"]
                st.session_state.navigation_reasoning = result["navigation_reasoning"]
                st.session_state.sql_explanation = result["sql_explanation"]
                st.session_state.corrected = result["corrected"]
            except Exception as e:
                st.error(f"Failed to generate SQL: {e}")

if st.session_state.sql:
    st.subheader("Generated SQL")
    st.caption(f"Grounded in wiki pages: {', '.join(st.session_state.pages_used)}")
    if st.session_state.corrected:
        st.warning(
            "The first attempt failed schema validation and had to be auto-corrected — "
            "logged to `wiki/corrections.md` for `wiki_agent.py` to review next run."
        )
    edited_sql = st.text_area("SQL (editable before running)", value=st.session_state.sql, height=150)

    with st.expander("How the agent got here", expanded=False):
        st.markdown("**Why these wiki pages were chosen:**")
        st.write(st.session_state.navigation_reasoning or "_(model gave no explanation)_")

        st.markdown("**Pages actually read:**")
        for link in st.session_state.pages_used:
            with st.expander(f"`{link}`"):
                page_text = load_wiki_page(link)
                st.markdown(page_text if page_text else "_(page not found)_")

        st.markdown("**Why this SQL:**")
        st.write(st.session_state.sql_explanation or "_(model gave no explanation)_")

    run_clicked = st.button("Run query", use_container_width=True)

    should_run = run_clicked or (auto_run and generate_clicked)
    if should_run:
        with st.spinner("Running query against Postgres..."):
            try:
                columns, rows = run_sql(edited_sql)
                st.subheader("Results")
                if rows:
                    st.dataframe(pd.DataFrame(rows, columns=columns), use_container_width=True)
                else:
                    st.info("Query ran successfully (no rows returned).")
            except Exception as e:
                st.error(f"Query failed: {e}")

with st.expander("Show wiki context for a table"):
    selected = st.selectbox("Table", sorted(docs))
    if selected:
        st.markdown(docs[selected])
