import duckdb

conn = duckdb.connect("ipl.duckdb")

print("Building player_bowling_match...")

conn.execute("""
DROP TABLE IF EXISTS player_bowling_match
""")

conn.execute("""
CREATE TABLE player_bowling_match AS

SELECT
    match_id,
    bowler AS player_name,

    COUNT(*) AS balls_bowled,

    ROUND(
        COUNT(*) / 6.0,
        1
    ) AS overs,

    SUM(runs_total) AS runs_conceded,

    SUM(
        CASE
            WHEN wicket_flag = 1
                 AND wicket_type NOT IN
                 ('run out',
                  'retired hurt',
                  'obstructing the field')
            THEN 1
            ELSE 0
        END
    ) AS wickets,

    ROUND(
        SUM(runs_total) * 1.0 /
        NULLIF(
            COUNT(*) / 6.0,
            0
        ),
        2
    ) AS economy

FROM deliveries_v2

GROUP BY
    match_id,
    bowler
""")

count = conn.execute("""
SELECT COUNT(*)
FROM player_bowling_match
""").fetchone()[0]

print()
print("player_bowling_match created successfully")
print(f"Rows: {count:,}")

conn.close()