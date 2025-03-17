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

        # Extract required sections
        section1 = df.iloc[0:9, df.columns.get_loc("D"): df.columns.get_loc("P") + 1]
        section2 = df.iloc[9:11, df.columns.get_loc("I"): df.columns.get_loc("P") + 1]
        section3 = df.iloc[16:25, df.columns.get_loc("K"): df.columns.get_loc("L") + 1]

        # Show data sections
        st.subheader("📊 Section 1: D-P (Rows 1-9)")
        st.dataframe(section1)
        csv1 = section1.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Section 1", csv1, "section1.csv", "text/csv")

        st.subheader("📊 Section 2: I-P (Rows 10-11)")
        st.dataframe(section2)
        csv2 = section2.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Section 2", csv2, "section2.csv", "text/csv")

        st.subheader("📊 Section 3: K-L (Rows 17-25)")
        st.dataframe(section3)
        csv3 = section3.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Section 3", csv3, "section3.csv", "text/csv")

        # Store uploaded file in session
        st.session_state.uploaded_files[uploaded_file.name] = df
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")

# 📩 Contact Me Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("📧 Email: **m.asdz@yahoo.com**")
    st.write("📞 Phone: **+989367267241**")
