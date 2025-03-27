import os
import json
import re

# Define the root directory containing all the metadata files
ROOT_DIR = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA"

# Trait types to check
TRAIT_TYPES = ["Background", "Armor", "Cloak", "Headgear", "Weapon"]

# Function to clean spaces from trait values
def clean_trait_value(value):
    # Remove extra spaces from start & end, and fix double spaces inside
    return re.sub(r'\s+', ' ', value.strip())

# Function to update metadata files
def clean_metadata():
    for folder_name in os.listdir(ROOT_DIR):
        folder_path = os.path.join(ROOT_DIR, folder_name)
        metadata_path = os.path.join(folder_path, "metadata")
        if not os.path.exists(metadata_path):
            continue

        for filename in os.listdir(metadata_path):
            if filename.endswith(".json"):
                filepath = os.path.join(metadata_path, filename)

                # Load metadata file
                with open(filepath, 'r', encoding="utf-8") as file:
                    metadata = json.load(file)

                attributes = metadata.get("attributes", [])
                updated = False  # Track if we make any changes

                for trait in attributes:
                    if trait["trait_type"] in TRAIT_TYPES:
                        cleaned_value = clean_trait_value(trait["value"])
                        if cleaned_value != trait["value"]:  # Only update if different
                            trait["value"] = cleaned_value
                            updated = True

                # Save the cleaned metadata only if changes were made
                if updated:
                    with open(filepath, 'w', encoding="utf-8") as file:
                        json.dump(metadata, file, indent=4)

    print("✅ Metadata cleaned! All extra spaces removed.")

# Run the script
clean_metadata()
