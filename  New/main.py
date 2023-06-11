import os
import shutil
target_directory = 'Documents'

# Create the target directory if it doesn't exist
os.makedirs(target_directory, exist_ok=True)

# Define the target directory to organize
target_directory = 'Documents'  # Update the target directory name

# Create a dictionary to map file extensions to folder names
extension_to_folder = {
    '.txt': 'Text Files',
    '.pdf': 'PDFs',
    '.jpg': 'Images',
    '.mp3': 'Music',
    '.docx': 'Ms',
    # Add more file extensions and corresponding folder names as needed
}

try:
    # Check if the target directory exists
    if os.path.exists(target_directory):
        # Iterate over the files in the target directory
        for filename in os.listdir(target_directory):
            if os.path.isfile(os.path.join(target_directory, filename)):
                # Get the file extension
                file_extension = os.path.splitext(filename)[1]

                # Check if the file extension is mapped to a folder
                if file_extension in extension_to_folder:
                    # Create the destination folder if it doesn't exist
                    folder_name = extension_to_folder[file_extension]
                    destination_folder = os.path.join(target_directory, folder_name)
                    os.makedirs(destination_folder, exist_ok=True)

                    # Move the file to the destination folder
                    source_path = os.path.join(target_directory, filename)
                    destination_path = os.path.join(destination_folder, filename)
                    shutil.move(source_path, destination_path)
                    print(f"Moved '{filename}' to '{folder_name}' folder.")
    else:
        print(f"The '{target_directory}' directory does not exist.")
except FileNotFoundError:
    print(f"The '{target_directory}' directory was not found.")

print("File organization complete.")
