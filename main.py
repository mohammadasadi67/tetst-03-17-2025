import os
import streamlit as st
import pandas as pd

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
        device_total_production = 0
        device_total_waste_kg = 0
        device_total_waste_package = 0

        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            xl = pd.ExcelFile(file_path)  # Load Excel file
            sheet_name = xl.sheet_names[0]  # Assume data is in the first sheet
            df = xl.parse(sheet_name)

            # Check if columns 'I' to 'P' exist in the dataframe
            if all(col in df.columns for col in ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']):
                # Sum the Total Production from column J (J10:J12)
                total_production = df.loc[9:11, 'J'].sum()
                device_total_production += total_production

                # Sum the Waste (L for waste/kg, M for waste/package)
                total_waste_kg = df.loc[9:11, 'L'].sum()
                device_total_waste_kg += total_waste_kg

                total_waste_package = df.loc[9:11, 'M'].sum()
                device_total_waste_package += total_waste_package

            else:
                st.warning(f"⚠️ The required columns 'I' to 'P' are missing in {file_name}.")

        # Store totals for each device
        total_data[device_name] = {
            "Total Production": device_total_production,
            "Total Waste (kg)": device_total_waste_kg,
            "Total Waste (Package)": device_total_waste_package
        }

    # Display summary of totals
    st.subheader("📊 Summary of Totals per Device")
    st.write(total_data)

    # Create a bar chart for the total data
    production_data = {device: data["Total Production"] for device, data in total_data.items()}
    waste_kg_data = {device: data["Total Waste (kg)"] for device, data in total_data.items()}
    waste_package_data = {device: data["Total Waste (Package)"] for device, data in total_data.items()}

    st.subheader("📊 Production vs Waste (kg and Package)")
    st.bar_chart(production_data, use_container_width=True)
    st.bar_chart(waste_kg_data, use_container_width=True)
    st.bar_chart(waste_package_data, use_container_width=True)

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
