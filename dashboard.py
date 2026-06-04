import streamlit as st
import duckdb

from utils.theme import apply_theme

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)



def show_table(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    st.dataframe(df, use_container_width=True)

conn = duckdb.connect("ipl.duckdb")

# apply_theme()

st.title("🏏 IPL Analytics Dashboard")
st.caption("Built By Abhishek Patel")

# KPI SECTION

matches = conn.execute(
    "SELECT COUNT(*) FROM matches"
).fetchone()[0]

deliveries = conn.execute(
    "SELECT COUNT(*) FROM deliveries_v2"
).fetchone()[0]

players = conn.execute(
    "SELECT COUNT(*) FROM players"
).fetchone()[0]

teams = conn.execute(
    "SELECT COUNT(*) FROM teams"
).fetchone()[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Matches", f"{matches:,}")

with c2:
    st.metric("Deliveries", f"{deliveries:,}")

with c3:
    st.metric("Players", f"{players:,}")

with c4:
    st.metric("Teams", f"{teams:,}")

# TEAMS

st.divider()
st.header("🏆 IPL Teams")

teams_df = conn.execute("""
SELECT team_name
FROM teams
ORDER BY team_name
""").df()

show_table(teams_df)

# RECENT MATCHES

st.divider()
st.header("📅 Recent Matches")

recent_df = conn.execute("""
SELECT
    season,
    date,
    team1,
    team2,
    winner
FROM matches
ORDER BY date DESC
LIMIT 20
""").df()

show_table(recent_df)

# TOP BATTERS

st.divider()
st.header("🏏 Top Batters")

top_batters = conn.execute("""
SELECT
    player_name,
    SUM(runs) AS runs,
    SUM(balls) AS balls,
    SUM(fours) AS fours,
    SUM(sixes) AS sixes,
    ROUND(
        SUM(runs) * 100.0 /
        NULLIF(SUM(balls),0),
        2
    ) AS strike_rate
FROM player_batting_match
GROUP BY player_name
HAVING SUM(runs) >= 500
ORDER BY runs DESC
LIMIT 10
""").df()

show_table(top_batters)

st.bar_chart(
    top_batters.set_index("player_name")["runs"]
)

# TOP BOWLERS

st.divider()
st.header("🎯 Top Bowlers")

top_bowlers = conn.execute("""
SELECT
    player_name,
    SUM(wickets) AS wickets,
    ROUND(AVG(economy),2) AS economy,
    ROUND(SUM(overs),1) AS overs
FROM player_bowling_match
GROUP BY player_name
HAVING SUM(wickets) >= 20
ORDER BY wickets DESC
LIMIT 10
""").df()

show_table(top_bowlers)

st.bar_chart(
    top_bowlers.set_index("player_name")["wickets"]
)

# TEAM PERFORMANCE

st.divider()
st.header("📈 Team Performance")

team_stats = conn.execute("""
WITH all_matches AS (

    SELECT
        team1 AS team,
        CASE
            WHEN winner = team1 THEN 1
            ELSE 0
        END AS win
    FROM matches

    UNION ALL

    SELECT
        team2 AS team,
        CASE
            WHEN winner = team2 THEN 1
            ELSE 0
        END AS win
    FROM matches

)

SELECT
    team,
    COUNT(*) AS matches,
    SUM(win) AS wins,
    ROUND(
        SUM(win) * 100.0 /
        COUNT(*),
        2
    ) AS win_pct
FROM all_matches
GROUP BY team
ORDER BY wins DESC
""").df()

show_table(team_stats)

st.bar_chart(
    team_stats.set_index("team")["wins"]
)

conn.close()