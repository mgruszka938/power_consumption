-- Energy used per day, in kWh.
--
-- Global_active_power is the average power during one minute, in kW.
-- One reading therefore stands for kW * (1/60) hours, so a day's energy
-- is the sum of its readings divided by 60.
--
-- SUM and COUNT(column) skip NULLs, so a day with missing readings
-- under-counts. The readings column shows how complete each day is
-- (1440 = a full day).
SELECT
    date(datetime)                            AS day,
    ROUND(SUM(Global_active_power) / 60.0, 2) AS kwh,
    COUNT(Global_active_power)                AS readings
FROM readings
GROUP BY day
ORDER BY day;
