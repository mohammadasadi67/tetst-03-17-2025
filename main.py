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
        file_names = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls"))]
        if file_names:
            st.sidebar.write("\n".join(file_names))
        else:
            st.sidebar.write("(No files uploaded yet)")

# 📤 Upload Tab
with tab2:
    st.title("📤 Upload & Select Data")

    uploaded_files = st.file_uploader("📂 Choose Excel files", type=["xlsx", "xls"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            xl = pd.ExcelFile(uploaded_file)  # Load Excel file
            file_name = uploaded_file.name

            # Determine folder based on file name suffix
            if file_name.endswith("125.xlsx"):
                target_folder = archive_folders["archive_125"]
            elif file_name.endswith("1000.xlsx"):
                target_folder = archive_folders["archive_1000"]
            elif file_name.endswith("200.xlsx"):
                target_folder = archive_folders["archive_200"]
            elif file_name.endswith("GASTI.xlsx"):
                target_folder = archive_folders["archive_gasti"]
            else:
