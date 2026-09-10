# 🗄️ LLM Wiki SQL Agent

Two-agent system that turns a raw PostgreSQL database into a browsable knowledge-graph wiki, then answers natural-language questions by grounding SQL generation in that wiki instead of the raw schema.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791) ![Groq](https://img.shields.io/badge/Groq-LLM%20inference-orange)

## 📌 Overview

Most NL-to-SQL tools hand an LLM the raw `information_schema` and hope it guesses what a column actually means. This project does something different:

1. A **Wiki Agent** introspects the live PostgreSQL schema and uses an LLM to write a full documentation wiki — one page per table, per foreign-key relationship, per business domain, per enum's allowed values — plus an ERD and a glossary, as an interlinked Obsidian vault.
2. A **SQL Agent** answers questions by reading `wiki/index.md`, picking only the wiki pages relevant to the question, and writing a SELECT-only SQL query grounded in what those pages say — not the raw schema.

The result: a self-documenting database where humans (browsing the Obsidian graph) and the SQL agent share the same source of truth.

## 🕸️ Knowledge Graph

<img width="701" height="504" alt="graph_wiki" src="https://github.com/user-attachments/assets/326820f1-58c3-41d5-85ba-0d557a5f1f95" />


The wiki agent generates 120+ cross-linked Markdown pages from a real procurement/sales/vendor-management schema (vendors, purchase orders, sales orders, sites, items, shipments, pricing...) — browsable as a fully connected knowledge graph in Obsidian.

## ✨ Features

- 🔍 **Schema introspection** — walks PostgreSQL `information_schema` for tables, columns, types, and foreign keys
- 📚 **Auto-generated wiki** — LLM writes entity, relationship, domain, and enum docs from the live schema
- 🕸️ **Knowledge graph** — wiki pages are cross-linked Markdown, browsable as a graph in Obsidian
- 🗺️ **ERD & glossary** — auto-generated entity-relationship diagram and business glossary
- 💬 **Wiki-grounded NL→SQL** — the SQL agent reads only the pages relevant to a question instead of dumping the whole schema into the prompt
- 🛡️ **SELECT-only execution** — generated SQL is restricted to read-only queries before running
- 🖥️ **Streamlit UI** — ask questions in plain English, see the generated SQL and results
- 📝 **Correction log** — the wiki tracks corrections/archive so documentation improves over time

## 🏗️ Architecture

```
        PostgreSQL Database
                │
      ┌─────────┴──────────┐
      │  db_introspect.py   │   schema introspection
      │ (tables, columns,   │   (information_schema)
      │  FKs, constraints)  │
      └─────────┬───────────┘
                ↓
         ┌───────────────┐
         │ wiki_agent.py │   Groq LLM (Qwen)
         └───────┬────────┘
                ↓
     wiki/  (Obsidian vault)
     ├── entities/        — one page per table
     ├── relationships/   — FK relationships
     ├── domains/         — business groupings
     ├── enums/           — allowed-value glossaries
     ├── queries/         — canonical query patterns
     └── erd.md · glossary.md · index.md
                ↓
      ┌─────────────────────┐
      │ sql_query_agent.py  │   reads wiki/index.md →
      │   (Groq / OpenAI)   │   picks relevant pages →
      └──────────┬──────────┘   writes SELECT-only SQL
                ↓
          streamlit_app.py
   "Show the 5 most recent growth
    opportunity events at Phoenix"
        → SQL + live results
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| PostgreSQL + psycopg2 | Source database, introspection & query execution |
| Groq API | LLM inference for wiki generation (Qwen) and the SQL agent |
| Streamlit | Interactive NL → SQL UI |
| Obsidian | Renders the generated wiki as a knowledge graph |

## 📁 Project Structure

```
db_introspect.py           # PostgreSQL schema introspection
dbconnection.py            # psycopg2 connection (env-configured)
wiki_agent.py               # generates wiki/ knowledge graph from the live schema
sql_query_agent.py          # wiki-grounded NL → SQL agent
streamlit_app.py             # Streamlit UI
create_dummy_tables*.py     # seed scripts for a demo procurement/sales schema
wiki/
  entities/  relationships/  domains/  enums/  queries/
  erd.md  glossary.md  index.md  conventions.md  overview.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A PostgreSQL database
- Groq API key (free at console.groq.com)

### Installation
```bash
git clone https://github.com/vijaya-842/LLM-WIKI-SQL-AGENT.git
cd LLM-WIKI-SQL-AGENT
pip install -r requirements.txt
```

### Configuration
Create a `.env` file:
```
PGHOST=localhost
PGPORT=5432
PGDATABASE=your_db
PGUSER=your_user
PGPASSWORD=your_password
GROQ_API_KEY=your_groq_api_key
```

### Generate the wiki
```bash
python wiki_agent.py
```

### Ask questions
```bash
streamlit run streamlit_app.py
```

## 🔮 Roadmap
- [ ] Cloud deployment (currently runs against a self-hosted/local PostgreSQL instance)
- [ ] Incremental wiki refresh on schema changes
- [ ] Multi-database support

## 🧠 What I Learned
- Grounding an NL→SQL agent in curated documentation instead of raw schema meaningfully improves accuracy on ambiguous business terms
- Chaining two agents where one agent's output (the wiki) becomes the other's retrieval context
- Using Obsidian's graph view to visualize and sanity-check LLM-generated schema documentation
- Restricting LLM-generated SQL to SELECT-only for safe execution against a live database

## 👩‍💻 Author

**Vijaya Lakshmi Atluri** — [GitHub](https://github.com/vijaya-842) · [LinkedIn](https://www.linkedin.com/in/vijaya-atluri/)

⭐ If you found this useful, consider starring the repo!
