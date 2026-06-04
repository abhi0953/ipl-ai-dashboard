import duckdb

conn = duckdb.connect("ipl.duckdb")

conn.execute("""
UPDATE matches
SET team1 =
CASE
    WHEN team1='Royal Challengers Bangalore' THEN 'Royal Challengers Bengaluru'
    WHEN team1='Delhi Daredevils' THEN 'Delhi Capitals'
    WHEN team1='Kings XI Punjab' THEN 'Punjab Kings'
    WHEN team1='Rising Pune Supergiants' THEN 'Rising Pune Supergiant'
    ELSE team1
END
""")

conn.execute("""
UPDATE matches
SET team2 =
CASE
    WHEN team2='Royal Challengers Bangalore' THEN 'Royal Challengers Bengaluru'
    WHEN team2='Delhi Daredevils' THEN 'Delhi Capitals'
    WHEN team2='Kings XI Punjab' THEN 'Punjab Kings'
    WHEN team2='Rising Pune Supergiants' THEN 'Rising Pune Supergiant'
    ELSE team2
END
""")

conn.execute("""
UPDATE matches
SET winner =
CASE
    WHEN winner='Royal Challengers Bangalore' THEN 'Royal Challengers Bengaluru'
    WHEN winner='Delhi Daredevils' THEN 'Delhi Capitals'
    WHEN winner='Kings XI Punjab' THEN 'Punjab Kings'
    WHEN winner='Rising Pune Supergiants' THEN 'Rising Pune Supergiant'
    ELSE winner
END
""")

print("Team names normalized successfully.")

conn.close()