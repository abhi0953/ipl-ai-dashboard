import streamlit as st
import duckdb
from utils.filters import get_filters

st.set_page_config(
    page_title="Batting Analytics",
    page_icon="🏏",
    layout="wide"
)

def show_table(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    st.dataframe(df, use_container_width=True)

conn = duckdb.connect("ipl.duckdb")

filters = get_filters()

st.title("🏏 Batting Analytics")

st.info(
    f"Season: {filters['season']} | "
    f"Team: {filters['team']} | "
    f"Player: {filters['player']}"
)

# --------------------------------
# Orange Cap Leaders
# --------------------------------

st.header("🟠 Orange Cap Leaders")

orange_cap = conn.execute("""
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

ORDER BY runs DESC

LIMIT 25
""").df()

show_table(orange_cap)

# --------------------------------
# Most Sixes
# --------------------------------

st.header("💥 Most Sixes")

sixes_df = conn.execute("""
SELECT
    player_name,
    SUM(sixes) AS sixes

FROM player_batting_match

GROUP BY player_name

ORDER BY sixes DESC

LIMIT 20
""").df()

show_table(sixes_df)

st.bar_chart(
    sixes_df.set_index("player_name")["sixes"]
)

# --------------------------------
# Most Fours
# --------------------------------

st.header("🏏 Most Fours")

fours_df = conn.execute("""
SELECT
    player_name,
    SUM(fours) AS fours

FROM player_batting_match

GROUP BY player_name

ORDER BY fours DESC

LIMIT 20
""").df()

show_table(fours_df)

st.bar_chart(
    fours_df.set_index("player_name")["fours"]
)

# --------------------------------
# High Strike Rate Players
# --------------------------------

st.header("⚡ Best Strike Rate (500+ Runs)")

sr_df = conn.execute("""
SELECT
    player_name,
    SUM(runs) AS runs,
    SUM(balls) AS balls,

    ROUND(
        SUM(runs) * 100.0 /
        NULLIF(SUM(balls),0),
        2
    ) AS strike_rate

FROM player_batting_match

GROUP BY player_name

HAVING SUM(runs) >= 500

ORDER BY strike_rate DESC

LIMIT 20
""").df()

show_table(sr_df)

conn.close()