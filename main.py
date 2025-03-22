import os
import streamlit as st
import pandas as pd

# Define folder names based on device names
device_folders = {
    "Device_125": "Archive_125",
    "Device_1000": "Archive_1000",
    "Device_200": "Archive_200",
    "Device_gasti": "Archive_gasti"
}

# Ensure that the archive folders exist
for folder in device_folders.values():
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

    # Show device folders in the sidebar
    st.sidebar.title("📂 Device Archives")
    total_data = {}

    for device_name, folder_path in device_folders.items():
        st.sidebar.subheader(device_name)

        # List files in each folder
        file_names = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls
