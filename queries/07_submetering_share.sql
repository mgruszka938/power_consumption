-- Where the electricity goes: share of total energy per sub-meter, by year.
--
-- Sub_metering_1..3 are watt-hours per minute (kitchen, laundry room,
-- water heater and air conditioner). Global_active_power is in kW, so
-- kW * 1000 / 60 gives the household total in the same unit, Wh per minute.
-- Whatever the three sub-meters do not measure is "other": total minus the
-- three, as described in the dataset documentation.
-- Only minutes where every value is present are used, and shares are
-- percentages so that the partial first and last years stay comparable.
WITH minutes AS (
    SELECT
        strftime('%Y', datetime)              AS year,
        Global_active_power * 1000 / 60.0     AS total_wh,
        Sub_metering_1                        AS kitchen_wh,
        Sub_metering_2                        AS laundry_wh,
        Sub_metering_3                        AS heating_wh
    FROM readings
    WHERE Global_active_power IS NOT NULL
      AND Sub_metering_1 IS NOT NULL
      AND Sub_metering_2 IS NOT NULL
      AND Sub_metering_3 IS NOT NULL
)
SELECT
    year,
    ROUND(100.0 * SUM(kitchen_wh) / SUM(total_wh), 1) AS kitchen_pct,
    ROUND(100.0 * SUM(laundry_wh) / SUM(total_wh), 1) AS laundry_pct,
    ROUND(100.0 * SUM(heating_wh) / SUM(total_wh), 1) AS heating_pct,
    ROUND(100.0 * (SUM(total_wh) - SUM(kitchen_wh) - SUM(laundry_wh) - SUM(heating_wh))
          / SUM(total_wh), 1)                         AS other_pct
FROM minutes
GROUP BY year
ORDER BY year;
