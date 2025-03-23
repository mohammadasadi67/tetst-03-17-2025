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

# Dictionary to hold categories
categories = {
    "1000": [],
    "125": [],
    "200": [],
    "gasti": []
}

# Function to extract date from the file name
def extract_date_from_filename(filename):
    return filename[:8]  # The date is assumed to be the first 8 characters

# Function to save the file into the category folder with the date appended to the file name
def save_file_to_category_folder(uploaded_file, category):
    # Get the date from the file name
    file_date = extract_date_from_filename(uploaded_file.name)
    
    # Define the folder path based on the category
    folder_path = f"./{category}_files"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the new file name with date included
    new_file_name = f"{file_date}_{uploaded_file.name}"
    
    # Save the file to the appropriate folder
    file_path = os.path.join(folder_path, new_file_name)

    # Write the file to the specified path
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

            # Check the category based on the file name (case-insensitive check)
            category = None
            file_name_lower = file_name.lower().replace(".xlsx", "")  # To handle case insensitivity and remove .xlsx

            # Check if file name ends with a category code (without .xlsx)
            if file_name_lower.endswith("1000cc"):
                category = "1000"
            elif file_name_lower.endswith("1000"):
                category = "1000"
            elif file_name_lower.endswith("200cc"):
                category = "200"
            elif file_name_lower.endswith("200"):
                category = "200"
            elif file_name_lower.endswith("125"):
                category = "125"
            elif file_name_lower.endswith("gasti"):
                category = "gasti"

            if category is None:
                st.error(f"File '{file_name}' does not belong to any known category.")
                continue

            # Add the file to its category list
            categories[category].append(uploaded_file)

            # Save the file to its respective folder with the date in the file name
            file_path = save_file_to_category_folder(uploaded_file, category)

            # Read the file with a loading indicator
            with st.spinner("Processing..."):
                try:
                    df = pd.read_excel(uploaded_file, sheet_name=0, header=None, engine="openpyxl")
                    st.success(f"File saved successfully to {file_path}!")
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
            st.write(f"Category: {category}")
            st.write(selected_data)

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
