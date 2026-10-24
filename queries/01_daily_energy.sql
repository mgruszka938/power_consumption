-- kWh per day. A reading is the average kW over one minute, so kWh = sum / 60.
SELECT
    date(datetime)                            AS day,
    ROUND(SUM(Global_active_power) / 60.0, 2) AS kwh,
    COUNT(Global_active_power)                AS readings
FROM readings
GROUP BY day
ORDER BY day;
