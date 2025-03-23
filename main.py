import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import datetime

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "upload", "archive", "contact me"])

# Define base directory for saving files
BASE_DIR = "uploaded_files"

# Ensure base directory exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# Dictionary to hold categories
categories = {
    "1000": [],
    "125": [],
    "200": [],
    "gasti": []
}

# Function to extract date from the file name
def extract_date_from_filename(filename):
    return filename[:8]  # Assumes the first 8 characters represent the date

# Function to save the file into the correct folder
def save_file_to_category_folder(uploaded_file, category):
    # Extract the date
    file_date = extract_date_from_filename(uploaded_file.name)

    # Define the category folder path
    folder_path = os.path.join(BASE_DIR, f"{category}_files")

    # Create the folder if it does not exist
    os.makedirs(folder_path, exist_ok=True)

    # New file name with date
    new_file_name = f"{file_date}_{uploaded_file.name}"
    file_path = os.path.join(folder_path, new_file_name)

    # Save the file properly
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

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

            # Determine category (case-insensitive)
            category = None
            file_name_lower = file_name.lower().replace(".xlsx", "")  # Remove .xlsx and make lowercase

            if file_name_lower.endswith("1000cc") or file_name_lower.endswith("1000"):
                category = "1000"
            elif file_name_lower.endswith("200cc") or file_name_lower.endswith("200"):
                category = "200"
            elif file_name_lower.endswith("125"):
                category = "125"
            elif file_name_lower.endswith("gasti"):
                category = "gasti"

            if category is None:
                st.error(f"File '{file_name}' does not belong to any known category.")
                continue

            # Save the file to the appropriate folder
            file_path = save_file_to_category_folder(uploaded_file, category)

            # Read the file with a loading indicator
            with st.spinner("Processing..."):
                try:
                    df = pd.read_excel(uploaded_file, sheet_name=0, header=None, engine="openpyxl")
                    st.success(f"File saved successfully to {file_path}!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    continue

            # Display category and file path
            st.write(f"Category: {category}")
            st.write(f"Saved file path: {file_path}")

# Archive Page
elif page == "archive":
    st.title("Archive")
    st.write("Your categories:")
    for category, files in categories.items():
        st.write(f"Category: {category}")
        if files:
            for file in files:
                st.write(f"File: {file.name}")
        else:
            st.write("No files uploaded for this category.")

# Contact Me Page
elif page == "contact me":
    st.title("All you need to contact me:")
    st.write("m.asdz@yahoo.com")
