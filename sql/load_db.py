"""
load_db.py
Loads data/students.csv into a SQLite database at db/students.db
using the schema defined in sql/schema.sql.

Run:
    python sql/load_db.py
"""

import sqlite3
import pandas as pd
import os

os.makedirs("db", exist_ok=True)
DB_PATH = "db/students.db"

conn = sqlite3.connect(DB_PATH)

with open("sql/schema.sql") as f:
    conn.executescript(f.read())

df = pd.read_csv("data/students.csv")
cols = df.columns.tolist()
placeholders = ",".join(["?"] * len(cols))
insert_sql = f"INSERT INTO students ({','.join(cols)}) VALUES ({placeholders})"
conn.executemany(insert_sql, df[cols].itertuples(index=False, name=None))

conn.commit()
count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
print(f"Loaded {count} rows into {DB_PATH}")

conn.close()
