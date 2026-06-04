import streamlit as st
import duckdb

st.set_page_config(
    page_title="Venue Analytics",
    page_icon="🏟",
    layout="wide"
)

def show_table(df):
    df = df.copy()
    df.index = range(1, len(df) + 1)
    st.dataframe(df, use_container_width=True)

conn = duckdb.connect("ipl.duckdb")

st.title("🏟 Venue Analytics")

st.header("🏟 Most Matches Hosted")

venues_df = conn.execute("""
SELECT
    venue,
    COUNT(*) AS matches
FROM matches
GROUP BY venue
ORDER BY matches DESC
LIMIT 25
""").df()

show_table(venues_df)

st.bar_chart(
    venues_df.set_index("venue")["matches"]
)

st.header("🏏 Highest Scoring Venues")

runs_df = conn.execute("""
SELECT
    m.venue,
    ROUND(AVG(d.runs_total),2) AS avg_runs_per_ball,
    COUNT(*) AS deliveries
FROM deliveries_v2 d
JOIN matches m
ON d.match_id = m.match_id
GROUP BY m.venue
HAVING COUNT(*) > 1000
ORDER BY avg_runs_per_ball DESC
LIMIT 25
""").df()

show_table(runs_df)

conn.close()