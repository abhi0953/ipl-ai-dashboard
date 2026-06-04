import duckdb

conn = duckdb.connect("ipl.duckdb")

cols = conn.execute("""
DESCRIBE matches
""").fetchall()

for col in cols:
    print(col)

conn.close()