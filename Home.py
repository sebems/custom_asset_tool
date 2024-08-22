"""
    This is the runner for the streamlit app. It provides a GUI to input assets in spreadsheet form and then allows for it export to a HaloITSM instance
"""
import streamlit as st

st.set_page_config("Home", page_icon="🚀")

st.sidebar.success("Select a page above.")

st.markdown("""
            ### Welcome to the Halo Asset Tool
            """)