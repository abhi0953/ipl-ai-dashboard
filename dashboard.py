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

st.title("🏏 IPL Analytics Dashboard")

st.markdown("""
### Analyze IPL History Like Never Before

Explore batting records, bowling performances, team statistics,
venue insights, and player profiles across IPL seasons.

📊 Data Coverage: 2008–2026
""")



st.markdown("---")

st.subheader("📌 Available Analytics")

col1, col2 = st.columns(2)

with col1:
    st.info("""
🏏 Batting Analytics

• Orange Cap Leaders
• Strike Rates
• Season Stats
• Player Comparisons
""")

with col2:
    st.info("""
🎯 Bowling Analytics

• Purple Cap Leaders
• Economy Rates
• Wicket Takers
• Season Stats
""")

col3, col4 = st.columns(2)

with col3:
    st.info("""
🏆 Team Analytics

• Head to Head
• Team Records
• Winning Stats
""")

with col4:
    st.info("""
👤 Player Profiles

• Career Stats
• Season Runs
• Top Venues
• Milestones
""")



# apply_theme()

st.title("🏏 IPL History")

# KPI SECTION

matches = conn.execute("""
SELECT COUNT(*) FROM matches
""").fetchone()[0]

players = conn.execute("""
SELECT COUNT(DISTINCT player_name)
FROM player_batting_match
""").fetchone()[0]

runs = conn.execute("""
SELECT SUM(runs)
FROM player_batting_match
""").fetchone()[0]

wickets = conn.execute("""
SELECT SUM(out_flag)
FROM player_batting_match
""").fetchone()[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏏 Matches", f"{matches:,}")

with col2:
    st.metric("👤 Players", f"{players:,}")

with col3:
    st.metric("🔥 Runs", f"{runs:,}")

with col4:
    st.metric("🎯 Wickets", f"{wickets:,}")



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

st.markdown("---")
st.subheader("🚀 Explore Analytics")

# Row 1
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.page_link(
            "pages/1_Batting.py",
            label=" Batting Analytics",
            icon="🏏"
        )

        st.caption(
            "Orange Cap • Strike Rate • Season Stats"
        )

with col2:
    with st.container(border=True):
        st.page_link(
            "pages/2_Bowling.py",
            label=" Bowling Analytics",
            icon="🎯"
        )

        st.caption(
            "Purple Cap • Economy • Wickets"
        )

# Row 2
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.page_link(
            "pages/3_Teams.py",
            label=" Team Analytics",
            icon="🏆"
        )

        st.caption(
            "Head-to-Head • Team Records"
        )

with col4:
    with st.container(border=True):
        st.page_link(
            "pages/4_Venues.py",
            label=" Venue Analytics",
            icon="🏟"
        )

        st.caption(
            "Venue Records • Ground Analysis"
        )

# Row 3
col5, col6 = st.columns(2)

with col5:
    with st.container(border=True):
        st.page_link(
            "pages/5_Player_Profile.py",
            label=" Player Analytics",
            icon="👤"
        )

        st.caption(
            "Career Stats • Milestones • Seasons"
        )

with col6:
    with st.container(border=True):
        st.markdown("###### 🔥 Coming Soon")

        st.caption(
            "Powerplay Analytics • Death Overs Analytics • AI Assistant"
        )
st.markdown("---")

st.caption(
    "Built by Abhishek Patel • IPL Analytics Dashboard"
)

conn.close()