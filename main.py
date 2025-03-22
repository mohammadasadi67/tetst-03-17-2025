import os
import streamlit as st
import pandas as pd

# تعریف پوشه‌های آرشیو
archive_folders = {
    "archive_125": "Archive_125",
    "archive_1000": "Archive_1000",
    "archive_200": "Archive_200",
    "archive_gasti": "Archive_gasti"
}

# ایجاد پوشه‌های آرشیو در صورت عدم وجود
for folder in archive_folders.values():
    if not os.path.exists(folder):
        os.makedirs(folder)

# تعریف تب‌ها
tab1, tab2, tab3 = st.tabs(["📊 Main", "📤 Upload", "📩 Contact Me"])

# 📂 تب اصلی (آرشیو)
with tab1:
    st.title("📂 آرشیو فایل‌ها")
    st.write("🔹 این بخش لیست فایل‌های ذخیره‌شده را نشان می‌دهد.")

    # نمایش فایل‌های هر پوشه
    st.sidebar.title("📂 لیست آرشیو")
    for folder_name, folder_path in archive_folders.items():
        st.sidebar.subheader(folder_name)

        files = [f for f in os.listdir(folder_path) if f.endswith((".xlsx", ".xls"))]
        for file_name in files:
            date_only = file_name.split(".")[0]  # فقط تاریخ را نمایش بده
            file_path = os.path.join(folder_path, file_name)

            # امکان دانلود فایل با کلیک روی نام آن
            st.sidebar.download_button(label=f"📅 {date_only}", 
                                       data=open(file_path, "rb").read(), 
                                       file_name=file_name, 
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 📤 تب آپلود (آپلود چندگانه)
with tab2:
    st.title("📤 آپلود فایل‌ها")
    st.write("🔹 فایل‌های اکسل خود را اینجا آپلود کنید.")

    # آپلود چندگانه فایل‌ها
    uploaded_files = st.file_uploader("📂 انتخاب فایل‌های اکسل", type=["xlsx", "xls"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name

            # تعیین پوشه ذخیره‌سازی بر اساس نام فایل
            if file_name.endswith("125.xlsx"):
                target_folder = archive_folders["archive_125"]
            elif file_name.endswith("1000.xlsx"):
                target_folder = archive_folders["archive_1000"]
            elif file_name.endswith("200.xlsx"):
                target_folder =_
