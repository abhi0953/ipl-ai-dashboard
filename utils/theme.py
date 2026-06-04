import streamlit as st

def apply_theme():

    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    col1, col2 = st.columns([8, 1])

    with col2:

        if st.session_state.dark_mode:
            label = "🌙 Dark"
        else:
            label = "☀️ Light"

        dark_mode = st.toggle(
            label,
            value=st.session_state.dark_mode
        )

        st.session_state.dark_mode = dark_mode

    if dark_mode:

        st.markdown(
            """
            <style>

            .stApp {
                background-color: #0f172a;
                color: white;
            }

            h1, h2, h3, h4, h5, h6,
            p, div, span, label {
                color: white !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <style>

            .stApp {
                background-color: white;
                color: black;
            }

            h1, h2, h3, h4, h5, h6,
            p, div, span, label {
                color: black !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )