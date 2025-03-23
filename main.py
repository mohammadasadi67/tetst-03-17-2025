import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

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
            
            # Determine file type based on name pattern
            if file_name.endswith("125.xlsx"):
                file_type = "Type 125"
            elif file_name.endswith("200.xlsx"):
                file_type = "Type 200"
            elif file_name.endswith("1000.xlsx"):
                file_type = "Type 1000"
            elif file_name.endswith("gasti.xlsx"):
                file_type = "Gasti Data"
            else:
                file_type = "Unknown Type"

            st.subheader(f"Processing: {file_name} ({file_type})")
            
            # Read the Excel file into a Pandas DataFrame
            df = pd.read_excel(uploaded_file)

            # Display DataFrame
            st.write(df.head())  # Show first few rows

# Archive Page
elif page == "archive":
    st.title("Archive")
    st.write("Your categories")

# Contact Me Page
elif page == "contact me":
    st.title("All you need to contact me:")
    st.write("m.asdz@yahoo.com")
