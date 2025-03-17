import streamlit as st
import pandas as pd
import os

# Initialize session state for storing uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

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


# Function to get folder name based on file name suffix
def get_folder_name(file_name):
    # Check if the filename is long enough (at least 8 characters for the date)
    if len(file_name) >= 12:
        suffix = file_name[-4:]  # Get the last 4 characters for the suffix (GASTI, 125, 1000, or 200)

        # Check if the suffix matches any known category
        if suffix == "125":
            return archive_folders["archive_125"]
        elif suffix == "1000":
            return archive_folders["archive_1000"]
        elif suffix == "200":
            return archive_folders["archive_200"]
        elif suffix == "GASTI":
            return archive_folders["archive_gasti"]
    return None


# Define tabs
tab1, tab2, tab3 = st.tabs(["📊 Main", "📤 Upload", "📩 Contact Me"])

# 🏠 Main Tab
with tab1:
    st.title("📊 Welcome to My Application")
    st.write("This app helps us track daily production issues, statistics, and analyze data for insights.")

    # Show archived files in the sidebar
    st.sidebar.title("📂 Archives")
    for folder_name, folder_path in archive_folders.items():
        if os.path.exists(folder_path):
            with st.sidebar.expander(folder_name):
                # List files in the folder
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(('.xlsx', '.xls')):
                        file_path = os.path.join(folder_path, file_name)
                        st.write(f"📄 {file_name}")

                        # Show preview of file in the sidebar
                        if file_name in st.session_state.uploaded_files:
                            df = st.session_state.uploaded_files[file_name]
                            st.write(df.head())  # Preview the first few rows

                        # Provide download option
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(f"⬇ Download {file_name}", csv, file_name, "text/csv")

                        # Option to delete the file
                        delete_button = st.button(f"❌ Delete {file_name}")
                        if delete_button:
                            # Delete the file from the file system and session state
                            if os.path.exists(file_path):
                                os.remove(file_path)
                                st.session_state.uploaded_files.pop(file_name, None)
                                st.success(f"✅ {file_name} deleted successfully!")
                            else:
                                st.error(f"⚠️ File {file_name} not found.")

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

        # Replace None/NaN with empty strings for display purposes
        df = df.where(pd.notnull(df), "")

        # Display the full sheet without filtering
        st.markdown("### 📊 Full Sheet Data")
        st.dataframe(df)

        # Provide download option
        csv_combined = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Full Sheet", csv_combined, "full_sheet.csv", "text/csv")

        # Get folder name based on the uploaded file's suffix
        folder_name = get_folder_name(uploaded_file.name)
        if folder_name:
            # Create the path to save the uploaded file in the appropriate folder
            save_path = os.path.join(folder_name, uploaded_file.name)

            # Save the file to the selected folder
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Store uploaded file in session
            st.session_state.uploaded_files[uploaded_file.name] = df
            st.success(f"✅ {uploaded_file.name} uploaded successfully to {folder_name}!")
        else:
            st.error("⚠️ File name does not match any known category.")

# 📩 Contact Me Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("📧 Email: **m.asdz@yahoo.com**")
    st.write("📞 Phone: **+989367267241**")
