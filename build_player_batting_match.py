import duckdb

conn = duckdb.connect("ipl.duckdb")

print("Building player_batting_match...")

conn.execute("""
DROP TABLE IF EXISTS player_batting_match
""")

conn.execute("""
CREATE TABLE player_batting_match AS

SELECT
    match_id,
    batter AS player_name,

    SUM(runs_batter) AS runs,
    COUNT(*) AS balls,

    SUM(
        CASE
            WHEN runs_batter = 4 THEN 1
            ELSE 0
        END
    ) AS fours,

    SUM(
        CASE
            WHEN runs_batter = 6 THEN 1
            ELSE 0
        END
    ) AS sixes,

    ROUND(
        SUM(runs_batter) * 100.0 /
        NULLIF(COUNT(*),0),
        2
    ) AS strike_rate,

    MAX(
        CASE
            WHEN player_dismissed = batter
            THEN 1
            ELSE 0
        END
    ) AS out_flag

FROM deliveries_v2

GROUP BY
    match_id,
    batter
""")

count = conn.execute("""
SELECT COUNT(*)
FROM player_batting_match
""").fetchone()[0]

print()
print("player_batting_match created successfully")
print(f"Rows: {count:,}")

conn.close()