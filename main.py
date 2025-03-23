import streamlit as st
from pathlib import Path

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Page 1", "Page 2"])

# Home Page
if page == "Home":
    st.title("Welcome to My Streamlit App")
    st.write("This is the home page.")

# Page 1
elif page == "Page 1":
    st.title("Page 1")
    st.write("This is the content of Page 1.")

# Page 2
elif page == "Page 2":
    st.title("Page 2")
    st.write("This is the content of Page 2.")
