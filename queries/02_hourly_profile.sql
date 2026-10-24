-- Average kW by hour of day, weekdays against weekends.
SELECT
    CAST(strftime('%H', datetime) AS INTEGER)                    AS hour,
    CASE WHEN strftime('%w', datetime) IN ('0', '6')
         THEN 'weekend' ELSE 'weekday' END                       AS day_type,
    ROUND(AVG(Global_active_power), 3)                           AS avg_kw
FROM readings
GROUP BY hour, day_type
ORDER BY day_type, hour;
