import os
import shutil

source_dir = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA"
destination_dir = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA\all_metadata"

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

for folder_name in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder_name)
    if os.path.isdir(folder_path):
        metadata_subfolder = os.path.join(folder_path, "metadata")
        if os.path.exists(metadata_subfolder):
            for file_name in os.listdir(metadata_subfolder):
                source_file = os.path.join(metadata_subfolder, file_name)
                destination_file = os.path.join(destination_dir, file_name)
                
                # Again, rename if needed to avoid duplicates
                shutil.copy2(source_file, destination_file)

print("All metadata have been copied into:", destination_dir)
