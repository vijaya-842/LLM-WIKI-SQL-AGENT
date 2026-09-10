import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("PGHOST", "localhost"),
    "port": os.environ.get("PGPORT", "5432"),
    "dbname": os.environ.get("PGDATABASE", "postgres"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", ""),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def test_connection():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print(cur.fetchone()[0])
        conn.close()
    except OperationalError as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    test_connection()
