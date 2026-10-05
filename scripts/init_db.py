"""Run once to create the SQLite database and tables: python scripts/init_db.py"""
from db import init_db, DB_PATH

if __name__ == "__main__":
    init_db()
    print(f"Database ready at {DB_PATH}")
