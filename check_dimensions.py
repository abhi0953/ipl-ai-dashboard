import duckdb

conn = duckdb.connect("ipl.duckdb")

for table in [
    "players",
    "teams",
    "venues",
    "seasons"
]:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(table, count)

conn.close()