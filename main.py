
import streamlit as st

# Define tabs
tab1, tab2, tab3 = st.tabs(["Main", "Upload", "Contact Me"])

# Main Tab
with tab1:
    st.title("Welcome to My Application")
    st.write(
        "This application helps us demonstrate daily production issues and statistics, and mine them in the near future.")

# Upload Tab
with tab2:
    st.title("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        # You can add code here to read the file with Pandas

# Contact Tab
with tab3:
    st.title("Contact Me")
    st.write("For any inquiries, contact me at: example@email.com")

# Sidebar - Archive Section
st.sidebar.title("📂 Archives")
st.sidebar.write("List of past reports will be displayed here.")

