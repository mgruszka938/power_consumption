import pandas as pd
import pytest

from household_power import data, db


def test_there_is_a_test_for_every_query_file():
    assert len(db.query_names()) == 8


# 04 needs 20 complete days per month, so it has its own test below
@pytest.mark.parametrize("name", [n for n in db.query_names() if not n.startswith("04")])
def test_query_runs(name, sample_db):
    assert len(db.run_query(name, sample_db)) > 0


def test_daily_energy_is_kwh(sample_db):
    daily = db.run_query("01_daily_energy", sample_db).set_index("day")
    assert daily.loc["2020-01-01", "kwh"] == 24.0
    assert daily.loc["2020-01-02", "kwh"] == 22.0
    assert daily.loc["2020-01-02", "readings"] == 1320


def test_incomplete_days_are_left_out_of_the_rolling_average(sample_db):
    days = db.run_query("05_rolling_7day", sample_db)["day"].tolist()
    assert days == ["2020-01-01", "2020-01-03"]


def test_missing_block_is_found(sample_db):
    blocks = db.run_query("08_missing_blocks", sample_db)
    assert len(blocks) == 1
    assert blocks.loc[0, "minutes"] == 120
    assert blocks.loc[0, "gap_start"] == "2020-01-02 01:00:00"


def test_submetering_shares_add_up(sample_db):
    row = db.run_query("07_submetering_share", sample_db).iloc[0]
    assert row["kitchen_pct"] == pytest.approx(60.0, abs=0.1)
    assert row[["kitchen_pct", "laundry_pct", "heating_pct", "other_pct"]].sum() == pytest.approx(100.0, abs=0.2)


def test_year_over_year_compares_the_same_month(tmp_path):
    # January 2020 at 1 kW, January 2021 at 2 kW
    frames = []
    for year, kw in ((2020, 1.0), (2021, 2.0)):
        index = pd.date_range(f"{year}-01-01", periods=25 * 1440, freq="min", name="datetime")
        frames.append(pd.DataFrame({col: kw for col in data.SENSOR_COLS}, index=index))
    path = tmp_path / "yoy.db"
    db.save_to_sqlite(pd.concat(frames), path)

    result = db.run_query("04_year_over_year", path).set_index("month")
    assert pd.isna(result.loc["2020-01", "yoy_pct"])
    assert result.loc["2021-01", "yoy_pct"] == 100.0
    assert result.loc["2021-01", "same_month_last_year"] == 24.0
