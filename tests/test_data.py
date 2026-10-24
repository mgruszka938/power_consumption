import numpy as np
import pandas as pd

from household_power import data


def series_with_gap(length):
    """Value 0 before the gap, value 100 after it, `length` missing minutes in between."""
    index = pd.date_range("2020-01-01", periods=length + 2, freq="min")
    values = [0.0] + [np.nan] * length + [100.0]
    return pd.Series(values, index=index)


def test_short_gap_is_interpolated():
    filled = data.fill_short_gaps(series_with_gap(3))
    assert filled.notna().all()
    assert filled.iloc[2] == 50.0  # linear: 0, 25, 50, 75, 100


def test_gap_of_exactly_the_limit_is_filled():
    assert data.fill_short_gaps(series_with_gap(60), max_minutes=60).notna().all()


def test_longer_gap_is_left_completely_empty():
    # Series.interpolate(limit=60) would fill the first 60 values of this gap.
    filled = data.fill_short_gaps(series_with_gap(61), max_minutes=60)
    assert filled.isna().sum() == 61


def test_gaps_at_the_edges_are_not_extrapolated():
    index = pd.date_range("2020-01-01", periods=5, freq="min")
    series = pd.Series([np.nan, 1.0, 2.0, 3.0, np.nan], index=index)
    filled = data.fill_short_gaps(series)
    assert np.isnan(filled.iloc[0]) and np.isnan(filled.iloc[-1])


def test_clean_drops_duplicates_sorts_and_indexes_by_time():
    raw = pd.DataFrame({
        "Date": ["2/1/2020", "1/1/2020", "1/1/2020", "1/1/2020"],
        "Time": ["00:00:00", "00:01:00", "00:00:00", "00:00:00"],
        **{col: [1.0, 2.0, 3.0, 3.0] for col in data.SENSOR_COLS},
    })
    cleaned = data.clean(raw)
    assert len(cleaned) == 3  # the exact duplicate row is gone
    assert cleaned.index.is_monotonic_increasing
    assert cleaned.index.name == "datetime"
    assert "Date" not in cleaned.columns and "Time" not in cleaned.columns


def test_check_quality_reports_missing_blocks():
    raw = pd.DataFrame({
        "Date": ["1/1/2020"] * 6,
        "Time": [f"00:0{i}:00" for i in range(6)],
        **{col: [1.0, np.nan, np.nan, 1.0, np.nan, 1.0] for col in data.SENSOR_COLS},
    })
    quality = data.check_quality(raw)
    assert quality["missing_rows"] == 3
    assert list(quality["missing_blocks"]) == [2, 1]
