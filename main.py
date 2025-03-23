import streamlit as st
import pandas as pd
import os
from io import BytesIO
import re

# Set up base directory to store files
BASE_DIR = "uploaded_files"
os.makedirs(BASE_DIR, exist_ok=True)

# Define categories based on filename pattern
CATEGORIES = ["1000", "1000cc", "200", "200cc", "125", "gasti"]

# Function to extract category from filename
def extract_category(filename):
    match = re.search(r"(\d{8})(1000|1000cc|200|200cc|125|gasti)", filename, re.IGNORECASE)
    if match:
        return match.group(2).lower()  # Ensure lowercase for consistency
    return None

# Function to extract date from filename
def extract_date_from_filename(filename):
    match = re.search(r"(\d{8})", filename)
    return match.group(1) if match else "unknown_date"

# Function to save file in the correct folder
def save_file_to_category_folder(uploaded_file, category):
    file_date = extract_date_from_filename(uploaded_file.name)
    folder_path = os.path.join(BASE_DIR, f"{category}_files")

    # Create category folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Define the full file path with date for tracking
    new_file_name = f"{file_date}_{uploaded_file.name}"
    file_path = os.path.join(folder_path, new_file_name)

    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved in: `{file_path}`")  # Display the saved path
    return file_path

# Streamlit UI
st.set_page_config(page_title="File Organizer", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload", "Archive"])

if page == "Upload":
    st.title("Upload Files and Organize Automatically")
    
    uploaded_files = st.file_uploader("Upload your Excel files", type=["xlsx"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            category = extract_category(file_name)

            if category:
                st.subheader(f"Processing: {file_name} (Category: {category})")
                save_file_to_category_folder(uploaded_file, category)
            else:
                st.error(f"File '{file_name}' does not belong to any known category.")

elif page == "Archive":
    st.title("File Archive")
    st.write("Your files are stored in the following folders:")
    
    for category in CATEGORIES:
        folder_path = os.path.join(BASE_DIR, f"{category}_files")
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            st.subheader(f"{category.upper()} Files:")
            for file in files:
                st.write(f"📂 {file}")
        else:
            st.warning(f"No files in {category} category yet.")
