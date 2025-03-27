import os
import shutil

# 1. Set up paths (adjust these to match your system)
source_dir = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA"
destination_dir = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA\all_images"

# 2. Create the destination folder if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# 3. Loop through each subfolder in the source directory
for folder_name in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder_name)

    # If it’s actually a folder (and not a file)
    if os.path.isdir(folder_path):
        # Construct the path to the images subfolder
        images_subfolder = os.path.join(folder_path, "images")

        # If that images subfolder exists, copy its contents
        if os.path.exists(images_subfolder):
            # Loop over each file in the images subfolder
            for file_name in os.listdir(images_subfolder):
                source_file = os.path.join(images_subfolder, file_name)
                destination_file = os.path.join(destination_dir, file_name)

                # If needed, rename the destination file to avoid overwriting duplicates
                # For example:
                # new_file_name = f"{folder_name}-{file_name}"
                # destination_file = os.path.join(destination_dir, new_file_name)
                
                # Copy the file (shutil.copy2 preserves metadata, timestamps, etc.)
                shutil.copy2(source_file, destination_file)

print("All images have been copied into:", destination_dir)
