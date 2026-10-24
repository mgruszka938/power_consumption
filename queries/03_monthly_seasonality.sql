-- Average kWh per day for each calendar month, complete days only (1440 readings).
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
