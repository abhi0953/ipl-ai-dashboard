import json
from pathlib import Path
import duckdb
import pandas as pd

DATA_DIR = Path("data")
DB_FILE = "ipl.duckdb"

print("Building dimensions...")

players = set()
teams = set()
venues = set()
seasons = set()

json_files = list(DATA_DIR.glob("*.json"))

for idx, file in enumerate(json_files, start=1):

    try:
        with open(file, "r", encoding="utf-8") as f:
            match = json.load(f)

        info = match.get("info", {})

        # Teams
        for team in info.get("teams", []):
            if team:
                teams.add(team)

        # Venue
        venue = info.get("venue")
        if venue:
            venues.add(venue)

        # Season
        season = info.get("season")
        if season:
            seasons.add(str(season))

        # Players from registry
        registry = info.get("registry", {})
        people = registry.get("people", {})

        for player_name in people.keys():
            players.add(player_name)

    except Exception as e:
        print(f"Error in {file.name}: {e}")

    if idx % 100 == 0:
        print(f"Processed {idx}/{len(json_files)}")

# Create dataframes
players_df = pd.DataFrame(
    {"player_name": sorted(players)}
)

teams_df = pd.DataFrame(
    {"team_name": sorted(teams)}
)

venues_df = pd.DataFrame(
    {"venue_name": sorted(venues)}
)

seasons_df = pd.DataFrame(
    {"season": sorted(seasons)}
)

# Normalize team names
teams_df["team_name"] = teams_df["team_name"].replace({
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiants": "Rising Pune Supergiant"
})

teams_df = teams_df.drop_duplicates()

conn = duckdb.connect(DB_FILE)

conn.execute("DROP TABLE IF EXISTS players")
conn.execute("DROP TABLE IF EXISTS teams")
conn.execute("DROP TABLE IF EXISTS venues")
conn.execute("DROP TABLE IF EXISTS seasons")

conn.register("players_df", players_df)
conn.register("teams_df", teams_df)
conn.register("venues_df", venues_df)
conn.register("seasons_df", seasons_df)

conn.execute("""
CREATE TABLE players AS
SELECT * FROM players_df
""")

conn.execute("""
CREATE TABLE teams AS
SELECT * FROM teams_df
""")

conn.execute("""
CREATE TABLE venues AS
SELECT * FROM venues_df
""")

conn.execute("""
CREATE TABLE seasons AS
SELECT * FROM seasons_df
""")

print()
print("Dimensions created successfully")
print(f"Players : {len(players_df):,}")
print(f"Teams   : {len(teams_df):,}")
print(f"Venues  : {len(venues_df):,}")
print(f"Seasons : {len(seasons_df):,}")

conn.close()