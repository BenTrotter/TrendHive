# file_operations.py

import os
import shutil

def rename_and_move_latest_file(downloads_folder, target_folder, new_filename):
    # Get list of files in the downloads folder
    files = [f for f in os.listdir(downloads_folder) if f.endswith(".mp4")]

    if not files:
        print("No MP4 files found in the downloads folder.")
        return

    # Get the full path to the files
    files = [os.path.join(downloads_folder, f) for f in files]

    # Get the most recent file by modification time
    latest_file = max(files, key=os.path.getmtime)

    # Define the target path with the new filename
    target_path = os.path.join(target_folder, new_filename)

    # Rename and move the file
    shutil.move(latest_file, target_path)
    print(f"Moved and renamed file to: {target_path}")
