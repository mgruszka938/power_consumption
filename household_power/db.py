import sqlite3
from pathlib import Path

import pandas as pd

from .data import SENSOR_COLS

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "power.db"
QUERY_DIR = ROOT / "queries"


def save_to_sqlite(cleaned, db_path=DB_PATH):
    db_path = Path(db_path)
    table = cleaned[SENSOR_COLS].reset_index()
    table["datetime"] = table["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # build in a temp file and rename, so a crash never leaves a half-written database
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
    sql = (QUERY_DIR / f"{name}.sql").read_text(encoding="utf-8")
    con = sqlite3.connect(f"file:{Path(db_path).as_posix()}?mode=ro", uri=True)
    try:
        return pd.read_sql_query(sql, con)
    finally:
        con.close()
