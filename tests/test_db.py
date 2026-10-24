import sqlite3
from unittest import mock

import pandas as pd
import pytest

from household_power import db

from conftest import make_cleaned


def test_save_creates_table_index_and_iso_timestamps(tmp_path):
    path = tmp_path / "t.db"
    db.save_to_sqlite(make_cleaned(days=1), path)
    con = sqlite3.connect(path)
    assert con.execute("SELECT COUNT(*) FROM readings").fetchone() == (1440,)
    assert con.execute("SELECT MIN(datetime) FROM readings").fetchone() == ("2020-01-01 00:00:00",)
    indexes = [row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type = 'index'")]
    assert indexes == ["idx_readings_datetime"]
    con.close()


def test_crash_does_not_leave_a_database_behind(tmp_path):
    path = tmp_path / "t.db"
    with mock.patch.object(pd.DataFrame, "to_sql", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError):
            db.save_to_sqlite(make_cleaned(days=1), path)
    assert not path.exists()


def test_rebuild_recovers_from_a_leftover_temp_file(tmp_path):
    path = tmp_path / "t.db"
    (tmp_path / "t.db.tmp").write_text("garbage")
    db.save_to_sqlite(make_cleaned(days=1), path)
    assert path.exists() and not (tmp_path / "t.db.tmp").exists()
