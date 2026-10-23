# Household Power Consumption Analysis

Cleaning and exploring four years of minute-by-minute electricity readings from one household, with Python and SQL.

The data is the UCI [Individual household electric power consumption](https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set) dataset: 2,075,259 readings from December 2006 to November 2010.

## What it does

1. **Imports** the dataset with `kagglehub` and loads it with pandas, treating `?` as missing.
2. **Checks quality:** duplicate rows, duplicate timestamps, missing values, and how long the gaps in the data are (the longest is about 5 days).
3. **Cleans:** removes duplicates, sorts by time, fills gaps of up to one hour by time-based interpolation and adds calendar features (hour, weekday, month, weekend).
4. **Plots** the distributions of power and voltage, and average usage by hour of day, day of week and month.
5. **Stores** the cleaned readings in a SQLite database (`power.db`) so they can be queried with SQL.

Gaps longer than an hour are deliberately left empty instead of invented. About 1.2% of the readings (25,151) are still missing after cleaning.

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

The first run downloads the dataset (about 130 MB). Running the script creates `power.db` in the project folder. The file is large, so it is not committed to Git.

To see the plots, uncomment the `plot_data` and `plot_profiles` calls in `main()`.

## The database

`power.db` has one table, `readings`, with one row per minute:

| Column | Type | Meaning |
|---|---|---|
| `datetime` | TEXT | Timestamp, `YYYY-MM-DD HH:MM:SS` |
| `Global_active_power` | REAL | Household active power (kW) |
| `Global_reactive_power` | REAL | Household reactive power (kW) |
| `Voltage` | REAL | Voltage (V) |
| `Global_intensity` | REAL | Current (A) |
| `Sub_metering_1` | REAL | Kitchen energy (Wh) |
| `Sub_metering_2` | REAL | Laundry room energy (Wh) |
| `Sub_metering_3` | REAL | Water heater and air conditioner energy (Wh) |

Missing readings are stored as `NULL`.

Try it:

```bash
sqlite3 power.db "SELECT datetime, Global_active_power FROM readings LIMIT 5;"
```

## Status

- [x] Data import, quality checks and cleaning
- [x] Exploratory plots
- [x] SQLite export
- [ ] SQL queries for daily usage, hourly profiles and data-quality reports
- [ ] Rolling averages and month-over-month trends with window functions
- [ ] Saved charts and findings in this README

## Built with

Python, pandas, seaborn, matplotlib and SQLite.
