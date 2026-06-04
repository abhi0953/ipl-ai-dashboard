import duckdb

conn = duckdb.connect("ipl.duckdb")

result = conn.execute("""
SELECT DISTINCT player_name
FROM player_batting_match
WHERE player_name LIKE '%Kohli%'
ORDER BY player_name
""").fetchall()

for row in result:
    print(row[0])

conn.close()