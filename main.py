import pandas
import os
import kagglehub

SENSOR_COLS = ["Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity",
               "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]

def data_import():
    DATA_PATH = kagglehub.dataset_download("uciml/electric-power-consumption-data-set")

    DTYPES = {
    "Global_active_power": "float32", "Global_reactive_power": "float32", "Voltage": "float32",
    "Global_intensity": "float32", "Sub_metering_1": "float32", "Sub_metering_2": "float32",
    "Sub_metering_3": "float32",
    }

    raw_data = pandas.read_csv(
    os.path.join(DATA_PATH, "household_power_consumption.txt"),
    sep=";",
    na_values=["?"], 
    dtype = DTYPES,
    low_memory=False
    )

    return raw_data

def data_check(raw_data):
    duplicate_rows = raw_data.duplicated()
    missing = raw_data.isna().sum()
    datetime_parsed = pandas.to_datetime(raw_data["Date"] + " " + raw_data["Time"], format="%d/%m/%Y %H:%M:%S")
    n_dup_timestamps = datetime_parsed.duplicated().sum()
    
    if n_dup_timestamps > 0:
        print(f"Duplicate timestamps found: {n_dup_timestamps}")
    else:
        print("No duplicate timestamps found.")

    if missing.any():
        print(f"Missing values found: {missing.sum()}")
    else:
        print("No missing values found.")

    if duplicate_rows.any():
        print(f"Duplicate rows found: {duplicate_rows.sum()}")
    else:
        print("No duplicate rows found.")

    na_mask = raw_data[SENSOR_COLS].isna().any(axis=1)
    change_points = na_mask.ne(na_mask.shift()).cumsum()
    missing_blocks = raw_data[na_mask].groupby(change_points[na_mask]).size()

    print(f"Number of contiguous missing-data blocks : {len(missing_blocks)}")
    print(f"Block length -- min / median / max (minutes) : {missing_blocks.min()} / {missing_blocks.median():.0f} / {missing_blocks.max()}")
    print()
    print("Longest 5 missing blocks (minutes):")
    print(missing_blocks.sort_values(ascending=False).head(5))

def data_cleanup(raw_data):
    raw_data = raw_data.drop_duplicates()
    raw_data = raw_data.dropna()

    return raw_data

def main():
    raw = data_import()
    data_check(raw)
    cleaned = data_cleanup(raw)

if __name__ == "__main__":
    main()


