import streamlit as st

def show_sidebar():

    with st.sidebar:

        st.markdown("# 🏏 IPL Analytics")
        st.caption("2008–2026 IPL Data")

        st.markdown("---")

        st.page_link(
            "dashboard.py",
            label="📊 Dashboard"
        )

        st.page_link(
            "pages/1_Batting.py",
            label="🏏 Batting Analytics"
        )

        st.page_link(
            "pages/2_Bowling.py",
            label="🎯 Bowling Analytics"
        )

        st.page_link(
            "pages/3_Teams.py",
            label="🏆 Team Analytics"
        )

        st.page_link(
            "pages/4_Venues.py",
            label="🏟 Venue Analytics"
        )

        st.page_link(
            "pages/5_Player_Profile.py",
            label="👤 Player Profiles"
        )

        

        st.info("""
### 🚀 Coming Soon

🔥 Powerplay Analytics

💀 Death Overs Analytics

🤖 AI Assistant
""")

        st.markdown("---")

        st.caption("Built by Abhishek Patel")