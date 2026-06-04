import json
from pathlib import Path
import duckdb
import pandas as pd

print("Starting IPL database build...")

DATA_DIR = Path("data")
DB_FILE = "ipl.duckdb"

conn = duckdb.connect(DB_FILE)

matches = []
deliveries = []

json_files = list(DATA_DIR.glob("*.json"))

print(f"Found {len(json_files)} match files")

for idx, file in enumerate(json_files, start=1):

    try:
        with open(file, "r", encoding="utf-8") as f:
            match = json.load(f)

        info = match.get("info", {})

        match_id = file.stem

        teams = info.get("teams", [])

        team1 = teams[0] if len(teams) > 0 else None
        team2 = teams[1] if len(teams) > 1 else None

        winner = (
            info.get("outcome", {})
            .get("winner")
        )

        matches.append({
            "match_id": match_id,
            "season": info.get("season"),
            "date": (
                info.get("dates", [None])[0]
                if info.get("dates")
                else None
            ),
            "venue": info.get("venue"),
            "city": info.get("city"),
            "team1": team1,
            "team2": team2,
            "winner": winner
        })

        innings_list = match.get("innings", [])

        for innings_no, innings in enumerate(innings_list, start=1):

            batting_team = innings.get("team")

            overs = innings.get("overs", [])

            for over in overs:

                over_no = over.get("over", 0)

                balls = over.get("deliveries", [])

                for ball_idx, ball in enumerate(balls, start=1):

                    runs = ball.get("runs", {})

                    wicket = None

                    if "wickets" in ball:
                        if len(ball["wickets"]) > 0:
                            wicket = ball["wickets"][0].get("kind")

                    deliveries.append({
                        "match_id": match_id,
                        "innings_no": innings_no,
                        "batting_team": batting_team,
                        "over_no": over_no,
                        "ball_no": ball_idx,
                        "batter": ball.get("batter"),
                        "bowler": ball.get("bowler"),
                        "runs_batter": runs.get("batter", 0),
                        "runs_total": runs.get("total", 0),
                        "wicket_type": wicket
                    })

        if idx % 50 == 0:
            print(f"Processed {idx}/{len(json_files)}")

    except Exception as e:
        print(f"Error in {file.name}: {e}")

matches_df = pd.DataFrame(matches)
deliveries_df = pd.DataFrame(deliveries)

conn.execute("DROP TABLE IF EXISTS matches")
conn.execute("DROP TABLE IF EXISTS deliveries")

conn.register("matches_df", matches_df)
conn.register("deliveries_df", deliveries_df)

conn.execute("""
CREATE TABLE matches AS
SELECT * FROM matches_df
""")

conn.execute("""
CREATE TABLE deliveries AS
SELECT * FROM deliveries_df
""")

print()
print("Database created successfully")
print(f"Matches: {len(matches_df):,}")
print(f"Deliveries: {len(deliveries_df):,}")
print("Database file: ipl.duckdb")

conn.close()