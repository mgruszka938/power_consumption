"""The SQLite database: building it from the cleaned data and querying it."""
import sqlite3
from pathlib import Path

import pandas as pd

from .data import SENSOR_COLS

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "power.db"
QUERY_DIR = ROOT / "queries"


def save_to_sqlite(cleaned, db_path=DB_PATH):
    """Write the readings table and its index to db_path.

    The database is built in a temporary file and renamed at the end, so db_path
    only ever exists as a complete database, even if this function crashes halfway.
    """
    db_path = Path(db_path)
    table = cleaned[SENSOR_COLS].reset_index()
    table["datetime"] = table["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")

    tmp_path = db_path.with_name(db_path.name + ".tmp")
    tmp_path.unlink(missing_ok=True)

    con = sqlite3.connect(tmp_path)
    try:
        table.to_sql("readings", con, if_exists="replace", index=False, chunksize=50_000)
        con.execute("CREATE INDEX idx_readings_datetime ON readings(datetime)")
        con.commit()
    finally:
        con.close()
    tmp_path.replace(db_path)


def query_names():
    return [path.stem for path in sorted(QUERY_DIR.glob("*.sql"))]


def run_query(name, db_path=DB_PATH):
    """Run queries/<name>.sql against the database and return a DataFrame."""
    sql = (QUERY_DIR / f"{name}.sql").read_text(encoding="utf-8")
    con = sqlite3.connect(f"file:{Path(db_path).as_posix()}?mode=ro", uri=True)
    try:
        return pd.read_sql_query(sql, con)
    finally:
        con.close()
