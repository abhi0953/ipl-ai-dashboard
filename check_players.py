import duckdb

conn = duckdb.connect("ipl.duckdb")

players = conn.execute("""
SELECT player_name
FROM players
ORDER BY player_name
LIMIT 50
""").fetchall()

for player in players:
    print(player[0])

conn.close()