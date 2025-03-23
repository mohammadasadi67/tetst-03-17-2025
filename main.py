import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Define category folders
CATEGORY_FOLDERS = {
    "1000": "1000",
    "1000cc": "1000",
    "125": "125",
    "200": "200",
    "200cc": "200",
    "gasti": "gasti",
    "Gasti": "gasti"
}

# Ensure main folders exist
for folder in set(CATEGORY_FOLDERS.values()):
    os.makedirs(folder, exist_ok=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "upload", "archive", "contact me"])

# Home Page
if page == "Home":
    st.title("Welcome to My Streamlit App")
    st.write("This is the home page.")

# Upload Page
elif page == "upload":
    st.title("Upload Source")
    st.write("Here you can upload your daily file")

    # File uploader
    uploaded_files = st.file_uploader("Upload your Excel files", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            st.subheader(f"Processing: {file_name}...")

            # Check file size
            if uploaded_file.size > 5_000_000:
                st.error("File is too large! Please upload a smaller file.")
                continue

            # Determine category based on filename
            category = None
            for key in CATEGORY_FOLDERS:
                if key in file_name:
                    category = CATEGORY_FOLDERS[key]
                    break

            if category is None:
                st.warning(f"Category not found for file: {file_name}. Skipping...")
                continue

            # Create subfolder for the category if not already present
            category_folder_path = os.path.join(category, file_name.split('.')[0])  # Subfolder inside category
            os.makedirs(category_folder_path, exist_ok=True)

            # Save file in the corresponding category subfolder
            save_path = os.path.join(category_folder_path, file_name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"File saved to {category_folder_path}/")

            # Read and process the file
            with st.spinner("Processing..."):
                try:
                    df = pd.read_excel(uploaded_file, sheet_name=0, header=None, engine="openpyxl")
                    st.success("File processed successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    continue

            # Show file shape (debugging)
            st.write(f"File shape: {df.shape}")

            # Ensure the file has enough data
            if df.shape[0] < 11 or df.shape[1] < 16:
                st.warning("File does not contain enough data for selection (I10:P11).")
                continue

            # Extract range I10:P11
            selected_data = df.iloc[9:11, 8:16]  # I=8, P=15 in zero-index

            # Display extracted data
            st.write(selected_data)

# Archive Page
elif page == "archive":
    st.title("Archive")
    st.write("Your categories")

# Contact Me Page
elif page == "contact me":
    st.title("All you need to contact me:")
    st.write("m.asdz@yahoo.com")
