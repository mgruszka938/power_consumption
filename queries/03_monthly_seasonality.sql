-- Average daily energy for each calendar month, over complete days only.
--
-- The CTE (WITH ... AS) computes one row per day first. Filtering on
-- readings = 1440 keeps only days with every minute present, which also
-- drops the partial first day of the dataset. A second GROUP BY then
-- averages those daily totals by month of the year.
WITH daily AS (
    SELECT
        date(datetime)             AS day,
        SUM(Global_active_power) / 60.0 AS kwh,
        COUNT(Global_active_power) AS readings
    FROM readings
    GROUP BY day
)
SELECT
    CAST(strftime('%m', day) AS INTEGER) AS month,
    ROUND(AVG(kwh), 2)                   AS avg_daily_kwh,
    COUNT(*)                             AS days
FROM daily
WHERE readings = 1440
GROUP BY month
ORDER BY month;
