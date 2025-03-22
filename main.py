import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define folder names based on device names
device_folders = {
    "Device_125": "Archive_125",
    "Device_1000": "Archive_1000",
    "Device_200": "Archive_200",
    "Device_gasti": "Archive_gasti"
}

# Ensure that the archive folders exist
for folder in device_folders.values():
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize session state for storing uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

# Define tabs
tab1, tab2, tab3 = st.tabs(["📊 Main", "📤 Upload", "📩 Contact Me"])

# 🏠 Main Tab
with tab1:
    st.title("📊 Welcome to My Application")
    st.write("This app helps us track daily production issues, statistics, and analyze data for insights.")

    # Show device folders in the sidebar
    st.sidebar.title("📂 Device Archives")
    total_data = {}

    for device_name, folder_path in device_folders.items():
        st.sidebar.subheader(device_name)

        # List files in each folder
        file_names = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls"))]
        if file_names:
            st.sidebar.write("\n".join(file_names))
        else:
            st.sidebar.write("(No files uploaded yet)")

        # Extract data from Excel files in the folder
        device_total = 0
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            xl = pd.ExcelFile(file_path)  # Load Excel file
            sheet_name = xl.sheet_names[0]  # Assume data is in the first sheet
            df = xl.parse(sheet_name)

            # Extract sum of values from columns I to P and rows 10 to 12
            sum_values = df.loc[9:11, 'I':'P'].sum().sum()  # Sum the range from I10:P12
            device_total += sum_values

        total_data[device_name] = device_total

    # Plotting the total data for each device
    st.subheader("📊 Total Data per Device")
    st.write(total_data)

    # Create a bar chart for the total data
    fig, ax = plt.subplots()
    ax.bar(total_data.keys(), total_data.values(), color='skyblue')
    ax.set_xlabel('Devices')
    ax.set_ylabel('Total Sum of Data')
    ax.set_title('Total Data per Device')
    st.pyplot(fig)

# 📤 Upload Tab
with tab2:
    st.title("📤 Upload & Select Data")

    uploaded_files = st.file_uploader("📂 Choose Excel files", type=["xlsx", "xls"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            xl = pd.ExcelFile(uploaded_file)  # Load Excel file
            file_name = uploaded_file.name

            # Determine folder based on file name suffix
            if file_name.endswith("125.xlsx"):
                target_folder = device_folders["Device_125"]
            elif file_name.endswith("1000.xlsx"):
                target_folder = device_folders["Device_1000"]
            elif file_name.endswith("200.xlsx"):
                target_folder = device_folders["Device_200"]
            elif file_name.endswith("GASTI.xlsx"):
                target_folder = device_folders["Device_gasti"]
            else:
                st.error("⚠️ File name does not match any known category.")
                target_folder = None

            if target_folder:
                # Save the file to the appropriate folder
                with open(os.path.join(target_folder, file_name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"✅ {file_name} uploaded successfully to {target_folder}.")
