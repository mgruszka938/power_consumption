-- The three highest-energy days of each calendar year.
--
-- RANK() numbers the days within each year (PARTITION BY year) from the
-- highest total down. The ranking is computed in a subquery because a
-- WHERE clause cannot filter on a window function directly.
WITH daily AS (
    SELECT
        date(datetime)             AS day,
        SUM(Global_active_power) / 60.0 AS kwh,
        COUNT(Global_active_power) AS readings
    FROM readings
    GROUP BY day
),
ranked AS (
    SELECT
        day,
        kwh,
        RANK() OVER (PARTITION BY strftime('%Y', day) ORDER BY kwh DESC) AS rank_in_year
    FROM daily
    WHERE readings = 1440
)
SELECT strftime('%Y', day) AS year, rank_in_year AS rank, day, ROUND(kwh, 2) AS kwh
FROM ranked
WHERE rank_in_year <= 3
ORDER BY year, rank;
