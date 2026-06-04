import streamlit as st
import duckdb

st.set_page_config(
    page_title="Team Analytics",
    page_icon="🏆",
    layout="wide"
)

conn = duckdb.connect("ipl.duckdb")

def show_table(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    st.dataframe(df, use_container_width=True)

st.title("🏆 Team Analytics")

# ---------------------------------
# TEAM RANKINGS
# ---------------------------------

st.header("🏆 Team Rankings")

team_rankings = conn.execute("""
WITH all_matches AS (

    SELECT
        team1 AS team,
        CASE WHEN winner = team1 THEN 1 ELSE 0 END AS win
    FROM matches

    UNION ALL

    SELECT
        team2 AS team,
        CASE WHEN winner = team2 THEN 1 ELSE 0 END AS win
    FROM matches

)

SELECT
    team,
    COUNT(*) AS matches,
    SUM(win) AS wins,
    ROUND(
        SUM(win) * 100.0 / COUNT(*),
        2
    ) AS win_pct

FROM all_matches

GROUP BY team

ORDER BY wins DESC
""").df()

show_table(team_rankings)

st.bar_chart(
    team_rankings.set_index("team")["wins"]
)

# ---------------------------------
# MOST MATCHES PLAYED
# ---------------------------------

st.header("🏏 Most Matches Played")

matches_df = conn.execute("""
WITH all_matches AS (

    SELECT team1 AS team
    FROM matches

    UNION ALL

    SELECT team2 AS team
    FROM matches

)

SELECT
    team,
    COUNT(*) AS matches

FROM all_matches

GROUP BY team

ORDER BY matches DESC
""").df()

show_table(matches_df)

# ---------------------------------
# HEAD TO HEAD
# ---------------------------------

st.divider()

st.header("⚔️ Head To Head")

teams = conn.execute("""
SELECT team_name
FROM teams
ORDER BY team_name
""").df()["team_name"].tolist()

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox(
        "Team 1",
        teams
    )

with col2:
    team2 = st.selectbox(
        "Team 2",
        teams,
        index=1
    )

if team1 != team2:

    h2h = conn.execute(f"""
    SELECT
        COUNT(*) AS matches,

        SUM(
            CASE
                WHEN winner = '{team1}'
                THEN 1
                ELSE 0
            END
        ) AS team1_wins,

        SUM(
            CASE
                WHEN winner = '{team2}'
                THEN 1
                ELSE 0
            END
        ) AS team2_wins,

        SUM(
            CASE
                WHEN winner IS NULL
                THEN 1
                ELSE 0
            END
        ) AS no_result

    FROM matches

    WHERE

    (
        team1 = '{team1}'
        AND team2 = '{team2}'
    )

    OR

    (
        team1 = '{team2}'
        AND team2 = '{team1}'
    )
    """).df()

    matches = int(h2h["matches"][0])
    team1_wins = int(h2h["team1_wins"][0])
    team2_wins = int(h2h["team2_wins"][0])
    no_result = int(h2h["no_result"][0])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Matches", matches)

    with c2:
        st.metric(
            f"{team1} Wins",
            team1_wins
        )

    with c3:
        st.metric(
            f"{team2} Wins",
            team2_wins
        )

    with c4:
        st.metric(
            "No Result",
            no_result
        )

    st.subheader("Recent Meetings")

    recent_matches = conn.execute(f"""
    SELECT
        date,
        season,
        team1,
        team2,
        winner,
        venue

    FROM matches

    WHERE

    (
        team1 = '{team1}'
        AND team2 = '{team2}'
    )

    OR

    (
        team1 = '{team2}'
        AND team2 = '{team1}'
    )

    ORDER BY date DESC

    LIMIT 10
    """).df()

    show_table(recent_matches)

conn.close()
