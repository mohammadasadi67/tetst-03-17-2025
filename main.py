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
    st.title("📤 Upload Excel File")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)  # Read file
        st.session_state.uploaded_files[uploaded_file.name] = df  # Store in session

        st.success(f"✅ {uploaded_file.name} uploaded successfully!")
        st.write("📊 **Data Preview:**")
        st.dataframe(df)  # Show data preview

# 📩 Contact Me Tab
with tab3:
    st.title("📩 Contact Me")
    st.write("📧 Email: **example@email.com**")
    st.write("📞 Phone: **+123456789**")

