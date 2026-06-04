import streamlit as st
import duckdb

st.set_page_config(
    page_title="Bowling Analytics",
    page_icon="🎯",
    layout="wide"
)

def show_table(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    st.dataframe(df, use_container_width=True)

conn = duckdb.connect("ipl.duckdb")

st.title("🎯 Bowling Analytics")

# --------------------------------
# Purple Cap Leaders
# --------------------------------

st.header("🟣 Purple Cap Leaders")

purple_cap = conn.execute("""
SELECT
    player_name,
    SUM(wickets) AS wickets,
    ROUND(AVG(economy),2) AS economy,
    ROUND(SUM(overs),1) AS overs,
    SUM(runs_conceded) AS runs_conceded

FROM player_bowling_match

GROUP BY player_name

ORDER BY wickets DESC

LIMIT 25
""").df()

show_table(purple_cap)

# --------------------------------
# Most Wickets
# --------------------------------

st.header("🏏 Most Wickets")

wickets_df = conn.execute("""
SELECT
    player_name,
    SUM(wickets) AS wickets

FROM player_bowling_match

GROUP BY player_name

ORDER BY wickets DESC

LIMIT 20
""").df()

show_table(wickets_df)

st.bar_chart(
    wickets_df.set_index("player_name")["wickets"]
)

# --------------------------------
# Best Economy
# --------------------------------

st.header("💰 Best Economy (100+ Overs)")

economy_df = conn.execute("""
SELECT
    player_name,

    ROUND(
        AVG(economy),
        2
    ) AS economy,

    ROUND(
        SUM(overs),
        1
    ) AS overs,

    SUM(wickets) AS wickets

FROM player_bowling_match

GROUP BY player_name

HAVING SUM(overs) >= 100

ORDER BY economy ASC

LIMIT 20
""").df()

show_table(economy_df)

# --------------------------------
# Most Overs Bowled
# --------------------------------

st.header("⏱ Most Overs Bowled")

overs_df = conn.execute("""
SELECT
    player_name,
    ROUND(SUM(overs),1) AS overs,
    SUM(wickets) AS wickets

FROM player_bowling_match

GROUP BY player_name

ORDER BY overs DESC

LIMIT 20
""").df()

show_table(overs_df)

st.bar_chart(
    overs_df.set_index("player_name")["overs"]
)

conn.close()