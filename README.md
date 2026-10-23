# Household Power Consumption Analysis

Cleaning and exploring four years of minute-by-minute electricity readings from one household, with Python and SQL.

The data is the UCI [Individual household electric power consumption](https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set) dataset: 2,075,259 readings from December 2006 to November 2010.

## What it does

1. **Imports** the dataset with `kagglehub` and loads it with pandas.
2. **Checks quality:** duplicate rows, duplicate timestamps, missing values, and how long the gaps in the data are (the longest is about 5 days).
3. **Cleans:** removes duplicates, sorts by time, fills gaps of up to one hour by time-based interpolation and adds calendar features (hour, weekday, month, weekend).
4. **Plots** the distributions of power and voltage, and average usage by hour of day, day of week and month.
5. **Stores** the cleaned readings in a SQLite database (`power.db`) so they can be queried with SQL.

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

The first run downloads the dataset (about 130 MB). Running the script creates `power.db` in the project folder.

To see the plots, uncomment the `plot_data` and `plot_profiles` calls in `main()`.

## Status

- [x] Data import, quality checks and cleaning
- [x] Exploratory plots
- [x] SQLite export
- [ ] SQL queries for daily usage, hourly profiles and data-quality reports
- [ ] Rolling averages and month-over-month trends with window functions
- [ ] Saved charts and findings in this README
