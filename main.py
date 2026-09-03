import pandas
import os
import kagglehub

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

    if missing.any():
        print(f"Missing values found: {missing.sum()}")
    else:
        print("No missing values found.")

    if duplicate_rows.any():
        print(f"Duplicate rows found: {duplicate_rows.sum()}")
    else:
        print("No duplicate rows found.")

def main():
    raw = data_import()
    data_check(raw)

if __name__ == "__main__":
    main()


