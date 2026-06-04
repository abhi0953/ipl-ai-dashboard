import duckdb

conn = duckdb.connect("ipl.duckdb")

matches = conn.execute(
    "SELECT COUNT(*) FROM matches"
).fetchone()[0]

deliveries = conn.execute(
    "SELECT COUNT(*) FROM deliveries"
).fetchone()[0]

print()
print("MATCHES:", matches)
print("DELIVERIES:", deliveries)

conn.close()