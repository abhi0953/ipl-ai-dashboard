import streamlit as st
import duckdb

def get_filters():

    conn = duckdb.connect("ipl.duckdb")

    seasons = conn.execute("""
    SELECT DISTINCT season
    FROM matches
    ORDER BY season
    """).df()["season"].tolist()

    teams = conn.execute("""
    SELECT team_name
    FROM teams
    ORDER BY team_name
    """).df()["team_name"].tolist()

    players = conn.execute("""
    SELECT player_name
    FROM players
    ORDER BY player_name
    """).df()["player_name"].tolist()

    conn.close()

    st.sidebar.header("🔍 Filters")

    season = st.sidebar.selectbox(
        "Season",
        ["All Seasons"] + seasons
    )

    team = st.sidebar.selectbox(
        "Team",
        ["All Teams"] + teams
    )

    player = st.sidebar.selectbox(
        "Player",
        ["All Players"] + players
    )

    return {
        "season": season,
        "team": team,
        "player": player
    }