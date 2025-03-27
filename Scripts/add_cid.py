import os
import json

# The main collection metadata folder CID.
IPFS_CID = "QmVeG135gSJ2VzgRmmHUiuZaCEme9nTd4qHtnvTuydTkfm"
# The gateway URL to be prepended.
GATEWAY = "https://white-determined-jaguar-140.mypinata.cloud/ipfs/"

metadata_dir = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA\all_metadata"

for filename in os.listdir(metadata_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(metadata_dir, filename)
        
        # Read the JSON metadata.
        with open(filepath, "r") as f:
            data = json.load(f)
        
        # Update the "image" field if it exists.
        if "image" in data:
            # Extract just the filename from the original image URI.
            # For example, if the original is "cypherpunk-1.png", it stays the same.
            # If it was "ipfs://QmVeG.../cypherpunk-1.png", we only need "cypherpunk-1.png".
            original_image = data["image"]
            image_filename = original_image.split("/")[-1]
            # Set the new image URL using the gateway.
            data["image"] = f"{GATEWAY}{IPFS_CID}/{image_filename}"
        
        # Update the "uri" field in properties.files if it exists.
        if "properties" in data and "files" in data["properties"]:
            for file_obj in data["properties"]["files"]:
                if "uri" in file_obj:
                    original_uri = file_obj["uri"]
                    file_name = original_uri.split("/")[-1]
                    file_obj["uri"] = f"{GATEWAY}{IPFS_CID}/{file_name}"
        
        # Save the updated JSON back to the file.
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

