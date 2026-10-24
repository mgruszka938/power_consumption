-- Average daily kWh per month against the same month a year earlier.
WITH daily AS (
    SELECT
        date(datetime)             AS day,
        SUM(Global_active_power) / 60.0 AS kwh,
        COUNT(Global_active_power) AS readings
    FROM readings
    GROUP BY day
),
monthly AS (
    SELECT
        strftime('%Y-%m', day) AS month,
        AVG(kwh)               AS avg_daily_kwh
    FROM daily
    WHERE readings = 1440
    GROUP BY month
    HAVING COUNT(*) >= 20
)
SELECT
    cur.month,
    ROUND(cur.avg_daily_kwh, 2)  AS avg_daily_kwh,
    ROUND(prev.avg_daily_kwh, 2) AS same_month_last_year,
    ROUND(100.0 * (cur.avg_daily_kwh - prev.avg_daily_kwh) / prev.avg_daily_kwh, 1) AS yoy_pct
FROM monthly AS cur
LEFT JOIN monthly AS prev
       ON prev.month = strftime('%Y-%m', cur.month || '-01', '-1 year')
ORDER BY cur.month;
