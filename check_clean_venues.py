import duckdb

conn = duckdb.connect("ipl.duckdb")

rows = conn.execute("""

SELECT
    venue_clean,
    COUNT(*)

FROM venue_mapping

GROUP BY venue_clean

ORDER BY COUNT(*) DESC

LIMIT 20

""").fetchall()

for row in rows:
    print(row)

conn.close()