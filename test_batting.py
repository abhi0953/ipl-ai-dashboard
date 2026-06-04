import duckdb

conn = duckdb.connect("ipl.duckdb")

print("\nTOP 10 RUN SCORERS\n")

result = conn.execute("""

SELECT
    player_name,
    SUM(runs) AS total_runs,
    SUM(balls) AS total_balls,
    ROUND(
        SUM(runs) * 100.0 /
        NULLIF(SUM(balls),0),
        2
    ) AS strike_rate

FROM player_batting_match

GROUP BY player_name

ORDER BY total_runs DESC

LIMIT 10

""").fetchall()

for row in result:
    print(row)

conn.close()