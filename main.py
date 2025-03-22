import os
import streamlit as st
import pandas as pd

# Initialize session state for storing uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

# Define tabs
tab1, tab2, tab3 = st.tabs(["📊 Main", "📤 Upload", "📩 Contact Me"])

# 🏠 Main Tab
with tab1:
    st.title("📊 Welcome to My Application")
    st.write("This app helps us track daily production issues, statistics, and analyze data for insights.")

# 📤 Upload Tab
with tab2:
    st.title("📤 Upload & Select Data")

    uploaded_files = st.file_uploader("📂 Choose Excel files", type=["xlsx", "xls"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            xl = pd.ExcelFile(uploaded_file)  # Load Excel file
            file_name = uploaded_file.name

            # Process each uploaded file (no archive functionality here)
            st.write(f"Processing file: {file_name}")

            # Example: Sum the production columns for rows 10 to 12 and columns I to P
            try:
                df = xl.parse(xl.sheet_names[0])  # Read the first sheet
                sum_values = df.loc[9:11, 'I':'P'].sum().sum()  # Sum the range from I10:P12
                st.write(f"Sum of total production (I10:P12) for {file_name}: {sum_values}")
            except Exception as e:
                st.error(f"Error processing {file_name}: {e}")

# 📩 Contact Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("For questions or feedback, please contact us!")
