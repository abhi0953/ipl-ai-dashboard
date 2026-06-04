import duckdb

conn = duckdb.connect("ipl.duckdb")

result = conn.execute("""
SELECT
    venue,
    COUNT(*) as matches
FROM matches
GROUP BY venue
ORDER BY matches DESC
LIMIT 10
""").fetchall()

for row in result:
    print(row)

conn.close()