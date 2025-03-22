import os
import shutil
import pandas as pd
import streamlit as st

# Define folder names based on file suffixes
archive_folders = [
    "Archive_125",
    "Archive_1000",
    "Archive_200",
    "Archive_gasti"
]

# Ensure that the archive folders exist (or create them if they don't exist)
for folder in archive_folders:
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
    for folder_name, folder_path in zip(["Archive_125", "Archive_1000", "Archive_200", "Archive_gasti"], archive_folders):
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
                target_folder = archive_folders[0]
            elif file_name.endswith("1000.xlsx"):
                target_folder = archive_folders[1]
            elif file_name.endswith("200.xlsx"):
                target_folder = archive_folders[2]
            elif file_name.endswith("GASTI.xlsx"):
                target_folder = archive_folders[3]
            else:
                st.error("⚠️ File name does not match any known category.")
                target_folder = None

            if target_folder:
                # Save file in the correct folder
                with open(os.path.join(target_folder, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File '{uploaded_file.name}' uploaded successfully to {target_folder}.")

    # 📂 Delete All Archives Section
    st.title("📂 Delete All Archives")
    delete_all_button = st.button("Delete All Archives")

    # If the button is clicked
    if delete_all_button:
        for folder in archive_folders:
            if os.path.exists(folder):
                try:
                    shutil.rmtree(folder)  # Delete the entire folder and its contents
                    st.success(f"Folder {folder} has been deleted successfully!")
                except Exception as e:
                    st.error(f"Error deleting folder {folder}: {e}")
            else:
                st.warning(f"Folder {folder} does not exist.")

# 📩 Contact Me Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("You can reach me at [m.asdz@yahoo.com](mailto:m.asdz@yahoo.com).")
