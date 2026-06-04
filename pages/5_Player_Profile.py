import streamlit as st
import duckdb

from utils.player_names import DISPLAY_NAMES

st.set_page_config(
    page_title="Player Profile",
    page_icon="👤",
    layout="wide"
)

conn = duckdb.connect("ipl.duckdb")

st.title("👤 Player Profile")

players = conn.execute("""
SELECT DISTINCT player_name
FROM player_batting_match
ORDER BY player_name
""").df()["player_name"].tolist()

vk_index = players.index("V Kohli")

selected_player = st.selectbox(
    "Search Player",
    players,
    index=vk_index
)

stats = conn.execute(f"""
SELECT
    COUNT(*) AS innings,
    SUM(runs) AS runs,
    SUM(balls) AS balls,
    SUM(fours) AS fours,
    SUM(sixes) AS sixes,

    MAX(runs) AS highest_score,

    SUM(
        CASE
            WHEN runs >= 50
            THEN 1
            ELSE 0
        END
    ) AS fifties,

    SUM(
        CASE
            WHEN runs >= 100
            THEN 1
            ELSE 0
        END
    ) AS hundreds

FROM player_batting_match

WHERE player_name = '{selected_player}'
""").df()

display_name = DISPLAY_NAMES.get(
    selected_player,
    selected_player
)

st.header(f"👤 {display_name}")

st.write("### Career Statistics")

runs = int(stats["runs"][0] or 0)
innings = int(stats["innings"][0] or 0)
balls = int(stats["balls"][0] or 0)
fours = int(stats["fours"][0] or 0)
sixes = int(stats["sixes"][0] or 0)
highest_score = int(stats["highest_score"][0] or 0)
fifties = int(stats["fifties"][0] or 0)
hundreds = int(stats["hundreds"][0] or 0)

strike_rate = round((runs * 100 / balls), 2) if balls > 0 else 0
avg_runs = round((runs / innings), 2) if innings > 0 else 0

st.write("🏏 Runs:", runs)
st.write("🎯 Innings:", innings)
st.write("⚡ Strike Rate:", strike_rate)
st.write("📈 Average Runs:", avg_runs)
st.write("4️⃣ Fours:", fours)
st.write("6️⃣ Sixes:", sixes)
st.write("🏆 Highest Score:", highest_score)
st.write("5️⃣0️⃣ Fifties:", fifties)
st.write("💯 Hundreds:", hundreds)

recent_df = conn.execute(f"""
SELECT
    m.season,
    m.team1 || ' vs ' || m.team2 AS match_name,
    p.runs,
    p.balls,
    p.fours,
    p.sixes

FROM player_batting_match p

JOIN matches m
ON p.match_id = m.match_id

WHERE p.player_name = '{selected_player}'

ORDER BY m.date DESC

LIMIT 10
""").df()

recent_df.index = range(1, len(recent_df) + 1)

st.write("### Recent Innings")

st.dataframe(
    recent_df,
    use_container_width=True
)

st.write("### Season-wise Runs")

season_df = conn.execute(f"""
SELECT
    m.season,
    SUM(p.runs) AS runs

FROM player_batting_match p

JOIN matches m
ON p.match_id = m.match_id

WHERE p.player_name = '{selected_player}'

GROUP BY m.season

ORDER BY m.season
""").df()

st.bar_chart(
    season_df.set_index("season")["runs"]
)

st.write("### 🏆 Best Seasons")

best_seasons = season_df.sort_values(
    "runs",
    ascending=False
)

best_seasons.index = range(
    1,
    len(best_seasons) + 1
)

st.dataframe(
    best_seasons,
    use_container_width=True
)

st.write("### ⚔️ Top Opponents")

opponent_df = conn.execute(f"""
SELECT
    CASE

        WHEN m.team1 LIKE '%Royal%'
        OR m.team2 LIKE '%Royal%'
        THEN 'Opponent'

        ELSE 'Opponent'

    END AS dummy,

    m.team1,
    m.team2,
    SUM(p.runs) AS runs

FROM player_batting_match p

JOIN matches m
ON p.match_id = m.match_id

WHERE p.player_name = '{selected_player}'

GROUP BY
    m.team1,
    m.team2

ORDER BY runs DESC

LIMIT 10
""").df()

opponent_df.index = range(1, len(opponent_df) + 1)

st.dataframe(
    opponent_df,
    use_container_width=True
)

st.write("### 🏟 Top Venues")

venue_df = conn.execute(f"""
SELECT
    vm.venue_clean AS venue,
    SUM(p.runs) AS runs

FROM player_batting_match p

JOIN matches m
ON p.match_id = m.match_id

JOIN venue_mapping vm
ON m.venue = vm.venue

WHERE p.player_name = '{selected_player}'

GROUP BY vm.venue_clean

ORDER BY runs DESC

LIMIT 10
""").df()

venue_df.index = range(1, len(venue_df) + 1)

st.dataframe(
    venue_df,
    use_container_width=True
)

st.bar_chart(
    venue_df.set_index("venue")["runs"]
)

conn.close()