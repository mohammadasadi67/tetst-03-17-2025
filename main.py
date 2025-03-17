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

        # Extract required sections using row range (11-23) and columns D to P
        section = df.iloc[10:23, 3:16]  # Rows 11 to 23, Columns D to P (indices 3 to 15)

        # Remove rows where all values are None
        section = section.dropna(how='all')

        # Styling: Set empty cells to black
        def highlight_empty_cells(val):
            color = 'black' if pd.isna(val) else 'white'  # If value is NaN, color it black
            return f'background-color: {color};'

        # Show the styled dataframe
        styled_df = section.style.applymap(highlight_empty_cells)

        # Display the styled dataframe
        st.markdown("### 📊 Data (Rows 11 to 23, Columns D to P)")
        st.dataframe(styled_df)

        # Provide download option
        csv_combined = section.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Data (Rows 11 to 23)", csv_combined, "data_11_to_23.csv", "text/csv")

        # Store uploaded file in session
        st.session_state.uploaded_files[uploaded_file.name] = df
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")

# 📩 Contact Me Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("📧 Email: **m.asdz@yahoo.com**")
    st.write("📞 Phone: **+989367267241**")
