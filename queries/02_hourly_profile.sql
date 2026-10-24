-- Average power by hour of the day, weekdays against weekends.
--
-- strftime('%H', ...) extracts the hour from the ISO text timestamp and
-- strftime('%w', ...) gives the weekday number (0 = Sunday, 6 = Saturday).
-- AVG ignores NULLs, so missing readings do not pull the average down.
SELECT
    CAST(strftime('%H', datetime) AS INTEGER)                    AS hour,
    CASE WHEN strftime('%w', datetime) IN ('0', '6')
         THEN 'weekend' ELSE 'weekday' END                       AS day_type,
    ROUND(AVG(Global_active_power), 3)                           AS avg_kw
FROM readings
GROUP BY hour, day_type
ORDER BY day_type, hour;
