import os
import streamlit as st
import pandas as pd

# Define folder names based on file suffixes
archive_folders = {
    "archive_125": "Archive_125",
    "archive_1000": "Archive_1000",
    "archive_200": "Archive_200",
    "archive_gasti": "Archive_gasti"
}

# Ensure that the archive folders exist
for folder in archive_folders.values():
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize session state for storing uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

# Define tabs
tab1, tab2, tab3 = st.tabs(["📊 Main", "📤 Upload", "📩 Contact Me"])

# 🏠 Main Tab
with tab1:
    st.title("📊 Welcome to My Application")
    st.write("This app helps us track daily production issues, statistics, and analyze data for insights.")

    # Show folders in the sidebar
    st.sidebar.title("📂 Archives")
    for folder_name, folder_path in archive_folders.items():
        st.sidebar.subheader(folder_name)

        # List files in each folder
        files = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls"))]
        for file_name in files:
            date_only =_
