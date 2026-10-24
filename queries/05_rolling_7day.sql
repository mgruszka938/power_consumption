-- Daily energy with a 7-day moving average.
--
-- A window function computes the average without collapsing the rows.
-- RANGE with a numeric day number covers the previous 6 days *by date*.
-- ROWS BETWEEN 6 PRECEDING would cover the previous 6 rows instead, which
-- stretches over more than a week wherever days were dropped for missing data.
WITH daily AS (
    SELECT
        date(datetime)             AS day,
        SUM(Global_active_power) / 60.0 AS kwh,
        COUNT(Global_active_power) AS readings
    FROM readings
    GROUP BY day
)
SELECT
    day,
    ROUND(kwh, 2) AS kwh,
    ROUND(AVG(kwh) OVER (
        ORDER BY julianday(day)
        RANGE BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS kwh_7d_avg
FROM daily
WHERE readings = 1440
ORDER BY day;
