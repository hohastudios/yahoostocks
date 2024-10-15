import streamlit as st

def menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("ui.py", label="Home")
    st.sidebar.page_link("pages/industry.py", label="Industry Analytics")