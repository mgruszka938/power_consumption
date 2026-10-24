import numpy as np
import pandas as pd
import pytest

from household_power import data, db


def make_cleaned(days=3, gap=None):
    index = pd.date_range("2020-01-01", periods=days * 1440, freq="min", name="datetime")
    frame = pd.DataFrame({col: 1.0 for col in data.SENSOR_COLS}, index=index)
    frame["Sub_metering_1"] = 10.0
    if gap is not None:
        start, length = gap
        frame.iloc[start:start + length] = np.nan
    return frame


@pytest.fixture
def sample_db(tmp_path):
    path = tmp_path / "sample.db"
    db.save_to_sqlite(make_cleaned(days=3, gap=(1440 + 60, 120)), path)
    return path
