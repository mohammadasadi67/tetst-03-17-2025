import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set page title
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Define category folders
CATEGORY_FOLDERS = {
    "1000": "1000",
    "125": "125",
    "200": "200",
    "Gasti": "Gasti"
}

# Ensure main folders exist
for folder in CATEGORY_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload", "Archive", "Contact Me"])

# Home Page
if page == "Home":
    st.title("Welcome to My Streamlit App")
    st.write("This is the home page.")

# Upload Page
elif page == "Upload":
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

            # Determine category based on filename
            category = None
            for key in CATEGORY_FOLDERS:
                if key.lower() in file_name.lower():
                    category = CATEGORY_FOLDERS[key]
                    break

            if category is None:
                st.warning(f"Category not found for file: {file_name}. Skipping...")
                continue

            # Save file in the corresponding category folder
            save_path = os.path.join(category, file_name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"File saved to {category}/")

            # Read and process the file
            with st.spinner("Processing..."):
                try:
                    df = pd.read_excel(uploaded_file, sheet_name=0, header=None, engine="openpyxl")
                    st.success("File processed successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    continue

            # Ensure the file has enough data
            if df.shape[0] < 11 or df.shape[1] < 16:
                st.warning("File does not contain enough data for selection (I10:P11).")
                continue

            # Extract range I10:P11
            selected_data = df.iloc[9:11, 8:16]  # I=8, P=15 in zero-index

            # Display extracted data
            st.write(selected_data)

    # **Download Section**
    st.subheader("Download Files from Archive")
    selected_category = st.selectbox("Select a category:", list(CATEGORY_FOLDERS.values()))

    if selected_category:
        category_path = os.path.join(selected_category)
        if os.path.exists(category_path):
            files_in_category = os.listdir(category_path)
            if files_in_category:
                selected_file = st.selectbox("Select a file:", files_in_category)
                if selected_file:
                    file_path = os.path.join(category_path, selected_file)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"Download {selected_file}",
                            data=f,
                            file_name=selected_file,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            else:
                st.warning("No files available in this category.")
        else:
            st.warning("Category folder does not exist.")

# Archive Page
elif page == "Archive":
    st.title("Archive")
    st.write("Your categorized files:")

    # Display files for each category
    for category, folder in CATEGORY_FOLDERS.items():
        st.subheader(f"{category} Files")

        # List files in the folder
        category_path = os.path.join(folder)
        if os.path.exists(category_path):
            files_in_category = os.listdir(category_path)
            if files_in_category:
                for file_name in files_in_category:
                    st.write(f"📄 {file_name}")
            else:
                st.write("No files available in this category.")
        else:
            st.warning(f"No folder found for category: {category}.")

# Contact Me Page
elif page == "Contact Me":
    st.title("All you need to contact me:")
    st.write("📧 m.asdz@yahoo.com")
