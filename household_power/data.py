"""Loading, checking and cleaning the UCI household power consumption data."""
import os

import kagglehub
import pandas as pd

DATASET = "uciml/electric-power-consumption-data-set"
RAW_FILE = "household_power_consumption.txt"

SENSOR_COLS = ["Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity",
               "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]

# Gaps up to this many minutes are filled by interpolation; longer ones stay empty.
MAX_FILL_MINUTES = 60


def load_raw():
    """Read the raw CSV (downloaded once by kagglehub, then served from its cache)."""
    folder = kagglehub.dataset_download(DATASET)
    dtypes = {col: "float32" for col in SENSOR_COLS}
    return pd.read_csv(
        os.path.join(folder, RAW_FILE),
        sep=";",
        na_values=["?"],
        dtype=dtypes,
        low_memory=False,
    )


def check_quality(raw):
    """Count duplicates and missing values, and measure the gaps in the data."""
    timestamps = pd.to_datetime(raw["Date"] + " " + raw["Time"], format="%d/%m/%Y %H:%M:%S")

    missing_row = raw[SENSOR_COLS].isna().any(axis=1)
    block_id = missing_row.ne(missing_row.shift()).cumsum()
    blocks = missing_row[missing_row].groupby(block_id[missing_row]).size()

    return {
        "rows": len(raw),
        "duplicate_rows": int(raw.duplicated().sum()),
        "duplicate_timestamps": int(timestamps.duplicated().sum()),
        "missing_rows": int(missing_row.sum()),
        "missing_blocks": blocks.sort_values(ascending=False),
    }


def fill_short_gaps(series, max_minutes=MAX_FILL_MINUTES):
    """Interpolate gaps of at most max_minutes and leave longer gaps empty.

    Series.interpolate(limit=n) is not enough: for a longer gap it still fills
    the first n values and leaves the rest empty, which invents data inside an
    outage. Here a gap is filled completely or not at all. Assumes one row per
    minute, so the number of missing rows in a gap is its length in minutes.
    """
    run_id = series.notna().cumsum()  # a gap shares its id with the value before it
    gap_length = series.isna().groupby(run_id).transform("sum")
    interpolated = series.interpolate(method="time", limit_area="inside")
    return interpolated.where(~(series.isna() & (gap_length > max_minutes)))


def clean(raw, max_fill_minutes=MAX_FILL_MINUTES):
    """Drop duplicates, index by timestamp, sort and fill short gaps."""
    data = raw.drop_duplicates().copy()
    data["datetime"] = pd.to_datetime(data["Date"] + " " + data["Time"], format="%d/%m/%Y %H:%M:%S")
    data = data.drop(columns=["Date", "Time"]).sort_values("datetime").set_index("datetime")

    for col in SENSOR_COLS:
        data[col] = fill_short_gaps(data[col], max_fill_minutes)

    return data
