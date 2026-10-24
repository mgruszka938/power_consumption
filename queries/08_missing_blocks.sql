-- Runs of consecutive missing readings, longest first (gaps and islands).
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
