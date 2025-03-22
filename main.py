import os

# Define archive folder paths
archive_folders = [
    "Archive_125",
    "Archive_1000",
    "Archive_200",
    "Archive_gasti"
]

# Delete all files inside each archive folder
for folder in archive_folders:
    if os.path.exists(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    else:
        print(f"{folder} folder does not exist.")
