import sys

import pytest

from household_power import __main__ as cli, db


def run(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["household_power", *args])
    cli.main()


@pytest.mark.parametrize("args", [("report",), ("query", "01_daily_energy")])
def test_missing_database_says_to_build_it(monkeypatch, tmp_path, capsys, args):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "missing.db")
    with pytest.raises(SystemExit) as exit_info:
        run(monkeypatch, *args)
    assert exit_info.value.code == 1
    assert "household_power build" in capsys.readouterr().err


def test_query_without_a_name_lists_queries_even_without_a_database(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "missing.db")
    run(monkeypatch, "query")
    assert "01_daily_energy" in capsys.readouterr().out
