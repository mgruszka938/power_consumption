import pandas
import os
import kagglehub
import matplotlib.pyplot as plt
import seaborn as sns

SENSOR_COLS = ["Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity",
               "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]

PALETTE = sns.color_palette("deep", 6)

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
    cleaned_data = raw_data.copy()
    cleaned_data = cleaned_data.drop_duplicates()

    datetime_parsed = pandas.to_datetime(cleaned_data["Date"] + " " + cleaned_data["Time"], format="%d/%m/%Y %H:%M:%S")
    cleaned_data["datetime"] = datetime_parsed
    cleaned_data = cleaned_data.sort_values("datetime").reset_index(drop=True)
    cleaned_data = cleaned_data.set_index("datetime")

    for col in SENSOR_COLS:
        cleaned_data[col] = cleaned_data[col].interpolate(method="time", limit= 60, limit_area = "inside")

    cleaned_data["year"] = cleaned_data.index.year
    cleaned_data["month"] = cleaned_data.index.month
    cleaned_data["day"] = cleaned_data.index.day
    cleaned_data["hour"] = cleaned_data.index.hour
    cleaned_data["minute"] = cleaned_data.index.minute
    cleaned_data["day_of_week"] = cleaned_data.index.dayofweek
    cleaned_data["day_name"] = cleaned_data.index.day_name()
    cleaned_data["week_of_year"] = cleaned_data.index.isocalendar().week.astype(int)
    cleaned_data["day_of_year"] = cleaned_data.index.dayofyear
    cleaned_data["quarter"] = cleaned_data.index.quarter
    cleaned_data["is_weekend"] = (cleaned_data["day_of_week"] >= 5).astype(int)

    return cleaned_data

def plot_data(cleaned_data):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.histplot(cleaned_data["Global_active_power"].dropna(), bins=80, color=PALETTE[3], ax=axes[0])
    axes[0].set_title("Global Active Power Distribution (minute-level)")
    axes[0].set_xlabel("Global Active Power (kW)"); axes[0].set_ylabel("Count")

    sns.boxplot(x=cleaned_data["Global_active_power"].dropna(), color=PALETTE[5], ax=axes[1])
    axes[1].set_title("Global Active Power — Box Plot")
    axes[1].set_xlabel("Global Active Power (kW)")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.histplot(cleaned_data["Voltage"].dropna(), bins=80, color=PALETTE[3], ax=axes[0])
    axes[0].set_title("Voltage Distribution (minute-level)")
    axes[0].set_xlabel("Voltage (V)"); axes[0].set_ylabel("Count")

    daily_voltage = cleaned_data["Voltage"].resample("D").mean()
    axes[1].plot(daily_voltage.index, daily_voltage.values, color=PALETTE[5], linewidth=0.7)
    axes[1].set_title("Daily Average Voltage Over Time")
    axes[1].set_xlabel("Date"); axes[1].set_ylabel("Voltage (V)")

    plt.tight_layout()
    plt.show()

def main():
    raw = data_import()
    data_check(raw)
    cleaned = data_cleanup(raw)
    plot_data(cleaned)


if __name__ == "__main__":
    main()


