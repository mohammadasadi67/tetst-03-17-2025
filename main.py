import os
import streamlit as st
import pandas as pd
import shutil

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

# Function to delete all archives
def delete_all_archives():
    for folder in archive_folders.values():
        if os.path.exists(folder):
            shutil.rmtree(folder)  # Delete the folder and its contents
            st.success(f"Deleted folder: {folder}")
        else:
            st.warning(f"Folder {folder} does not exist.")

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
                st.error("⚠️ File name does not match any known category.")
                target_folder = None

            # If a target folder is selected, save the file there
            if target_folder:
                file_path = os.path.join(target_folder, file_name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File {file_name} uploaded successfully to {target_folder}.")

    # Button to delete all archives
    delete_button = st.button("Delete All Archives")
    if delete_button:
        delete_all_archives()

# 📩 Contact Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("For questions or feedback, please contact us!")
