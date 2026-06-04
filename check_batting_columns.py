import duckdb

conn = duckdb.connect("ipl.duckdb")

result = conn.execute("""
DESCRIBE player_batting_match
""").fetchall()

for row in result:
    print(row)

conn.close()