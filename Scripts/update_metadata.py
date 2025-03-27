import os
import json

# Define the root directory containing all the etc-cypherpunks folders
ROOT_DIR = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA"

# Define rarity percentages for each tier
RARITY_TIERS = {
    "Legendary": 2,
    "Epic": 8,  # Updated from Ultra Rare to Epic
    "Rare": 20,
    "Uncommon": 30,
    "Common": 40,
    "None": 50  # For missing traits
}

# Define the percentage of NFTs that include each trait type
TRAIT_PERCENTAGES = {
    "Background": 100,
    "Bow": 100,
    "Armor": 100,
    "Cloak": 70,
    "Headgear": 60,
    "Companion": 50,
    "Weapon": 40,
}

# Function to calculate rarity score for an NFT
def calculate_rarity_score(attributes):
    score = 0
    for trait_type, percentage in TRAIT_PERCENTAGES.items():
        # Check if the trait exists in the NFT metadata
        matching_traits = [trait for trait in attributes if trait["trait_type"] == trait_type]

        if matching_traits:
            # Extract the tier name from the value (e.g., "Common", "Rare")
            tier_name = matching_traits[0]["value"].split()[0]  # Extract first word (e.g., "Legendary" from "Legendary Helmet")
            if tier_name in RARITY_TIERS:
                score += 100 / RARITY_TIERS[tier_name]
        else:
            # If the trait is missing, use the "None" tier
            score += 100 / RARITY_TIERS["None"]

    return round(score, 2)

# Update metadata files
def update_metadata():
    for folder_name in os.listdir(ROOT_DIR):
        folder_path = os.path.join(ROOT_DIR, folder_name)

        # Ensure the subfolder contains a metadata folder
        metadata_path = os.path.join(folder_path, "metadata")
        if not os.path.exists(metadata_path):
            continue

        print(f"Processing folder: {folder_name}")

        # Process all JSON files in the metadata folder
        for filename in os.listdir(metadata_path):
            if filename.endswith(".json"):
                filepath = os.path.join(metadata_path, filename)

                # Load the JSON metadata
                with open(filepath, 'r') as file:
                    metadata = json.load(file)

                # Add rarity score
                attributes = metadata.get("attributes", [])
                metadata["rarity_score"] = calculate_rarity_score(attributes)

                # Update creators field
                metadata["properties"]["creators"] = ["ETCMC"]

                # Remove compiler field
                if "compiler" in metadata:
                    del metadata["compiler"]

                # Save the updated file in place
                with open(filepath, 'w') as file:
                    json.dump(metadata, file, indent=4)

    print("All metadata files updated successfully!")

# Run the script
update_metadata()
