-- Every stretch of consecutive missing readings, longest first.
--
-- This is the "gaps and islands" pattern. Number all rows in time order
-- (rn), then keep only the missing rows and number those again. Window
-- functions run after WHERE, so the second counter only sees missing rows.
-- Within one unbroken stretch both counters grow by one per row, so their
-- difference stays constant; it jumps when a present row interrupts the
-- stretch. Grouping by that difference isolates each stretch.
WITH flagged AS (
    SELECT
        datetime,
        Global_active_power IS NULL           AS is_missing,
        ROW_NUMBER() OVER (ORDER BY datetime) AS rn
    FROM readings
),
missing AS (
    SELECT
        datetime,
        rn - ROW_NUMBER() OVER (ORDER BY datetime) AS block
    FROM flagged
    WHERE is_missing = 1
)
SELECT
    MIN(datetime)                 AS gap_start,
    MAX(datetime)                 AS gap_end,
    COUNT(*)                      AS minutes,
    ROUND(COUNT(*) / 1440.0, 1)   AS days
FROM missing
GROUP BY block
ORDER BY minutes DESC;
