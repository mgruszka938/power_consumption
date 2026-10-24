-- Daily kWh with a 7-day average. RANGE over the date keeps the window at 7 calendar days when days are missing.
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
