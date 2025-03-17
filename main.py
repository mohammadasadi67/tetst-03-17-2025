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

    # Show archived files in the sidebar
    st.sidebar.title("📂 Archives")
    if st.session_state.uploaded_files:
        for file_name, df in st.session_state.uploaded_files.items():
            with st.sidebar.expander(file_name):
                st.write(df.head())  # Show preview
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

        # Define the required areas
        required_rows = list(range(2, 9)) + list(range(10, 61))  # Rows 2-8, 10-60
        required_columns = list(range(3, 16))  # Columns D to P

        # Ensure row indices are within bounds
        valid_rows = [r for r in required_rows if r < len(df)]
        valid_cols = [c for c in required_columns if c < len(df.columns)]

        if valid_rows and valid_cols:
            extracted_data = df.iloc[valid_rows, valid_cols]
            extracted_data = extracted_data.dropna(how='all', axis=0)  # Remove fully empty rows

            # Display the extracted data
            st.markdown("### 📊 Extracted Data")
            st.dataframe(extracted_data)

            # Provide download option
            csv_combined = extracted_data.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download Extracted Data", csv_combined, "extracted_data.csv", "text/csv")
        else:
            st.error("❌ Selected indices are out of range. Please check your file.")

        # Store uploaded file in session
        st.session_state.uploaded_files[uploaded_file.name] = df
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")

# 📩 Contact Me Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("📧 Email: **m.asdz@yahoo.com**")
    st.write("📞 Phone: **+989367267241**")
