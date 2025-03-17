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


# Function to get folder name based on file name
def get_folder_name(file_name):
    if file_name.endswith("125"):
        return archive_folders["archive_125"]
    elif file_name.endswith("1000"):
        return archive_folders["archive_1000"]
    elif file_name.endswith("200"):
        return archive_folders["archive_200"]
    elif file_name.endswith("gasti"):
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
    if st.session_state.uploaded_files:
        for file_name, df in st.session_state.uploaded_files.items():
            with st.sidebar.expander(file_name):
                st.write(df.head())  # Show preview
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Download", csv, file_name, "text/csv")

                # Option to delete the file
                delete_button = st.button(f"❌ Delete {file_name}")
                if delete_button:
                    # Delete the file from the file system and session state
                    folder_name = get_folder_name(file_name)
                    if folder_name:
                        file_path = os.path.join(folder_name, file_name)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            st.session_state.uploaded_files.pop(file_name, None)
                            st.success(f"✅ {file_name} deleted successfully!")
                        else:
                            st.error(f"⚠️ File {file_name} not found.")
                    else:
                        st.error(f"⚠️ Could not determine folder for {file_name}.")

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

        # Decide the folder based on file name suffix
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
