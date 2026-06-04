import duckdb

conn = duckdb.connect("ipl.duckdb")

rows = conn.execute("""
SELECT DISTINCT venue
FROM matches
WHERE venue LIKE '%Chinnaswamy%'
ORDER BY venue
""").fetchall()

for row in rows:
    print(row[0])

conn.close()