# LLM Wiki on PostgreSQL DB

This project builds a knowledge wiki over a PostgreSQL-backed database using Python agents and Streamlit.

## Features
- Database introspection and schema exploration
- SQL query generation with an AI assistant
- Streamlit-based interface for interacting with the wiki
- Wiki content generation and management for database entities and relationships

## Requirements
Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run streamlit_app.py
```

## Project structure
- `db_introspect.py` – introspects database metadata
- `sql_query_agent.py` – SQL query agent logic
- `wiki_agent.py` – wiki generation logic
- `streamlit_app.py` – Streamlit web app
