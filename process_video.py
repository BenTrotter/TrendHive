
import os
import glob


def rename_latest_mp4_to_video():
    # Get the current directory
    current_directory = os.getcwd()
    # Find all .mp4 files in the current directory
    mp4_files = glob.glob(os.path.join(current_directory, "*.mp4"))
    if not mp4_files:
        print("No .mp4 files found in the current directory.")
        return
    # Find the latest .mp4 file by modification time
    latest_mp4_file = max(mp4_files, key=os.path.getmtime)
    # Define the target filename
    target_filename = os.path.join(current_directory, "video.mp4")
    # Check if "video.mp4" already exists, and remove it if it does
    if os.path.exists(target_filename):
        os.remove(target_filename)
        print(f"Existing file '{target_filename}' has been removed.")
    # Rename the latest .mp4 file to "video.mp4"
    os.rename(latest_mp4_file, target_filename)
    print(f"Renamed '{latest_mp4_file}' to '{target_filename}'.")