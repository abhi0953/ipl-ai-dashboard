import json
from pathlib import Path
import duckdb
import pandas as pd

DATA_DIR = Path("data")
DB_FILE = "ipl.duckdb"

print("Building deliveries_v2...")

records = []

json_files = list(DATA_DIR.glob("*.json"))

for idx, file in enumerate(json_files, start=1):

    try:
        with open(file, "r", encoding="utf-8") as f:
            match = json.load(f)

        match_id = file.stem

        innings_list = match.get("innings", [])

        for innings_no, innings in enumerate(innings_list, start=1):

            batting_team = innings.get("team")

            for over in innings.get("overs", []):

                over_no = over.get("over", 0)

                # Phase classification
                if over_no <= 5:
                    phase = "POWERPLAY"
                elif over_no <= 15:
                    phase = "MIDDLE"
                else:
                    phase = "DEATH"

                deliveries = over.get("deliveries", [])

                for ball_no, ball in enumerate(deliveries, start=1):

                    runs = ball.get("runs", {})
                    extras = ball.get("extras", {})

                    wicket_flag = 0
                    wicket_type = None
                    player_dismissed = None

                    if "wickets" in ball and len(ball["wickets"]) > 0:
                        wicket_flag = 1
                        wicket_type = ball["wickets"][0].get("kind")
                        player_dismissed = ball["wickets"][0].get("player_out")

                    records.append({
                        "match_id": match_id,
                        "innings_no": innings_no,
                        "batting_team": batting_team,

                        "over_no": over_no,
                        "ball_no": ball_no,

                        "phase": phase,

                        "batter": ball.get("batter"),
                        "bowler": ball.get("bowler"),
                        "non_striker": ball.get("non_striker"),

                        "runs_batter": runs.get("batter", 0),
                        "runs_extras": runs.get("extras", 0),
                        "runs_total": runs.get("total", 0),

                        "wides": extras.get("wides", 0),
                        "noballs": extras.get("noballs", 0),
                        "byes": extras.get("byes", 0),
                        "legbyes": extras.get("legbyes", 0),

                        "wicket_flag": wicket_flag,
                        "wicket_type": wicket_type,
                        "player_dismissed": player_dismissed
                    })

        if idx % 50 == 0:
            print(f"Processed {idx}/{len(json_files)}")

    except Exception as e:
        print(f"Error in {file.name}: {e}")

df = pd.DataFrame(records)

conn = duckdb.connect(DB_FILE)

conn.execute("""
DROP TABLE IF EXISTS deliveries_v2
""")

conn.register("deliveries_v2_df", df)

conn.execute("""
CREATE TABLE deliveries_v2 AS
SELECT * FROM deliveries_v2_df
""")

count = conn.execute("""
SELECT COUNT(*) FROM deliveries_v2
""").fetchone()[0]

print()
print("deliveries_v2 created successfully")
print(f"Rows: {count:,}")

conn.close()