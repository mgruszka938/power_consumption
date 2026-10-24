# Household power consumption

![tests](https://github.com/mgruszka938/power_consumption/actions/workflows/tests.yml/badge.svg)

An analysis of the UCI [household electric power consumption](https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set) dataset: 2,075,259 minute-level readings from one household, December 2006 to November 2010. I clean it with pandas, store it in SQLite and answer questions with SQL.

## Findings

Winter use is more than double summer use: 35.7 kWh a day in December against 13.7 in August.

![Daily energy use](figures/daily_energy.png)

From 6 to 30 August 2008 the daily total stays between 4.2 and 6.2 kWh, then goes back to 25.0 on the 31st. Probably an empty house, but the data can't say.

Weekdays peak at 7:00 and 21:00, weekends at 19:00.

![Average power by hour](figures/hourly_profile.png)

The water heater and air conditioner meter went from 31.1% of the energy in 2007 to 41.0% in 2010.

![Share of energy by sub-meter](figures/submetering.png)

## SQL

The eight queries in [`queries/`](queries) were checked against pandas on the full data.

| Query | Technique |
|---|---|
| `01_daily_energy` | GROUP BY |
| `02_hourly_profile` | strftime, CASE |
| `03_monthly_seasonality` | CTE |
| `04_year_over_year` | self join |
| `05_rolling_7day` | window function, RANGE |
| `06_top_days_per_year` | RANK, PARTITION BY |
| `07_submetering_share` | ratio of sums |
| `08_missing_blocks` | gaps and islands |

Timestamps are stored as `YYYY-MM-DD HH:MM:SS` text, with an index on the column.

## Run it

```bash
pip install -r requirements.txt
python -m household_power build
python -m household_power report
python -m household_power query 08_missing_blocks
```

Tests run offline on synthetic data:

```bash
pip install -r requirements-dev.txt
pytest
```
