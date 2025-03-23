import streamlit as st
from pathlib import Path

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "upload", "archive", "contact me"])

# Home Page
if page == "Home":
    st.title("Welcome to My Streamlit App")
    st.write("This is the home page.")

# upload
elif page == "upload":
    st.title("upload source")
    st.write("here you can upload your daily file")

# archive
elif page == "archive":
    st.title("archive")
    st.write("your categories")

# contact me
elif page == "contact me":
    st.title("all you need to contact me:")
    st.write("m.asdz@yahoo.com")
