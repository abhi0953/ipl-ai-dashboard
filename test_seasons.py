import duckdb

conn = duckdb.connect("ipl.duckdb")

result = conn.execute("""
SELECT DISTINCT season
FROM matches
ORDER BY season
""").fetchall()

for row in result:
    print(row[0])

conn.close()