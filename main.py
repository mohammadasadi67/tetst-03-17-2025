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
        for file_name in os.listdir(folder_path):
            if file_name.endswith((".xlsx", ".xls")):  # Check if it's an Excel file
                file_path = os.path.join(folder_path, file_name)
                with st.sidebar.expander(file_name):
                    df = pd.read_excel(file_path)  # Read the file
                    st.write(df.head())  # Display preview

                    # Provide a download button for the file
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇ Download", csv, file_name, "text/csv")

# 📤 Upload Tab
with tab2:
    st.title("📤 Upload & Select Data")

    uploaded_file = st.file_uploader("📂 Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        xl = pd.ExcelFile(uploaded_file)  # Load Excel file
        sheet_names = xl.sheet_names  # Get sheet names

        # Select sheet
        selected_sheet = st.selectbox("📑 Select Sheet", sheet_names)
        df = xl.parse(selected_sheet)  # Read selected sheet

        # Display the full sheet without filtering
        st.markdown("### 📊 Full Sheet Data")
        st.dataframe(df)

        # Provide download option
        csv_combined = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Full Sheet", csv_combined, "full_sheet.csv", "text/csv")

        # Determine folder based on file name suffix
        file_name = uploaded_file.name
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

        # Move the file to the correct folder and save it
        if target_folder:
            file_path = os.path.join(target_folder, file_name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.uploaded_files[file_name] = df
            st.success(f"✅ {uploaded_file.name} uploaded and saved to {target_folder}.")

# 📩 Contact Me Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("📧 Email: **m.asdz@yahoo.com**")
    st.write("📞 Phone: **+989367267241**")
