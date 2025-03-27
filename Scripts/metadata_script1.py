import os
import json

# Define the root directory containing all metadata files
ROOT_DIR = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA"

# Scaling factor to normalize rarity scores
SCALING_FACTOR = 20  # Adjust this if needed for a better scale

# Trait appearance probabilities
TRAIT_APPEARANCE_PROBABILITIES = {
    "Background": 1.00,  # Always present (100%)
    "Armor": 1.00,       # Always present (100%)
    "Cloak": 0.75,       # 75% of NFTs have a Cloak
    "Headgear": 0.70,    # 70% of NFTs have Headgear
    "Weapon": 0.65       # 65% of NFTs have a Weapon
}

# Bonuses for 4+ layers of the same tier
BONUS_PERCENTAGES = {
    "Common": 0.05,
    "Uncommon": 0.10,
    "Rare": 0.15,
    "Epic": 0.20,
    "Exquisite": 0.25,
    "Legendary": 0.30,
    "Mythic": 0.35,
}

# Special **Spirit** Bonus (Highest Priority)
SPIRIT_BONUS = 0.35  # 35% bonus if **any** item contains "Spirit"

# Frequencies for individual items (paste full list here)
ITEM_FREQUENCIES = {
    # Background
    "Common Background 1": 0.1076,
    "Common Background 2": 0.0962,
    "Common Background 3": 0.1020,
    "Common Background 4": 0.0968,
    "Uncommon Background 1": 0.0831,
    "Uncommon Background 2": 0.0799,
    "Uncommon Background 3": 0.0722,
    "Uncommon Background 4": 0.0683,
    "Rare Background 1": 0.0525,
    "Rare Background 2": 0.0498,
    "Rare Background 3": 0.0470,
    "Epic Background 1": 0.0327,
    "Epic Background 2": 0.0289,
    "Epic Background 3": 0.0243,
    "Exquisite Background 1": 0.0130,
    "Exquisite Background 2": 0.0109,
    "Exquisite Background 3": 0.0109,
    "Legendary Background 1": 0.0059,
    "Legendary Background 2": 0.0042,
    "Legendary Background 3": 0.0038,
    "Mythic Background": 0.0100,
        
    # Armor
    "Common Armor": 0.3492,
    "Uncommon Armor": 0.2547,
    "Rare Armor": 0.1743,
    "Epic Armor": 0.1042,
    "Exquisite Armor": 0.0757,
    "Legendary Armor": 0.0210,
    "Legendary Female Armor": 0.0109,
    "Mythic Armor": 0.0048,
    "Mythic Female Armor": 0.0050,
    "Mythic Male Spirit": 0.0001,
    "Mythic Female Spirit": 0.0001,
    
    #Cloak
    "Common Cloak 1": 0.0334,
    "Common Cloak 2": 0.0314,
    "Common Cloak 3": 0.0329,
    "Common Cloak 4": 0.0380,
    "Common Cloak 5": 0.0329,
    "Common Cloak 6": 0.0317,
    "Common Cloak 7": 0.0282,
    "Common Cloak 8": 0.0280,
    "Uncommon Cloak 1": 0.0281,
    "Uncommon Cloak 2": 0.0250,
    "Uncommon Cloak 3": 0.0236,
    "Uncommon Cloak 4": 0.0243,
    "Uncommon Cloak 5": 0.0252,
    "Uncommon Cloak 6": 0.0245,
    "Uncommon Cloak 7": 0.0262,
    "Uncommon Cloak 8": 0.0257,
    "Rare Cloak 1": 0.0180,
    "Rare Cloak 2": 0.0191,
    "Rare Cloak 3": 0.0153,
    "Rare Cloak 4": 0.0174,
    "Rare Cloak 5": 0.0142,
    "Rare Cloak 6": 0.0182,
    "Rare Cloak 7": 0.0173,
    "Rare Cloak 8": 0.0155,
    "Epic Cloak 1": 0.0129,
    "Epic Cloak 2": 0.0124,
    "Epic Cloak 3": 0.0128,
    "Epic Cloak 4": 0.0118,
    "Epic Cloak 5": 0.0131,
    "Epic Cloak 6": 0.0114,
    "Epic Cloak 7": 0.0085,
    "Epic Cloak 8": 0.0111,
    "Exquisite Cloak 1": 0.0077,
    "Exquisite Cloak 2": 0.0083,
    "Exquisite Cloak 3": 0.0071,
    "Exquisite Cloak 4": 0.0071,
    "Exquisite Cloak 5": 0.0058,
    "Exquisite Cloak 6": 0.0062,
    "Exquisite Cloak 7": 0.0057,
    "Exquisite Cloak 8": 0.0076,
    "Legendary Cloak 1": 0.0027,
    "Legendary Cloak 2": 0.0022,
    "Legendary Cloak 3": 0.0027,
    "Legendary Cloak 4": 0.0021,
    "Legendary Cloak 5": 0.0038,
    "Legendary Cloak 6": 0.0022,
    "Legendary Cloak 7": 0.0021,
    "Legendary Cloak 8": 0.0028,
    "Mythic Cloak 1": 0.0003,
    "Mythic Cloak 2": 0.0004,
    "Mythic Cloak 3": 0.0006,
    "Mythic Cloak 4": 0.0007,
    "Mythic Cloak 5": 0.0004,
    "Mythic Cloak 6": 0.0004,
    "Mythic Cloak 7": 0.0007,
    "Mythic Cloak 8": 0.0004,
    "Mythic Cloak 9": 0.0006,
    "Mythic Cloak 10": 0.0004,
    "Mythic Female Cloak 8": 0.0004,
    "Mythic Female Cloak 1": 0.0005,
    "Mythic Female Cloak 2": 0.0006,
    "Mythic Female Cloak 3": 0.0005,
    "Mythic Female Cloak 4": 0.0004,
    "Mythic Female Cloak 5": 0.0007,
    "Mythic Female Cloak 6": 0.0006,
    "Mythic Female Cloak 7": 0.0006,
    "Mythic Female Cloak 9": 0.0006,
    
    # Headgear 
    "Common Cowboy Hat": 0.0171,
    "Common Samurai Hat 1": 0.0214,
    "Common Respirator": 0.0196,
    "Common Helmet 1": 0.0153,
    "Common Punk Helmet 1": 0.0151,
    "Common Samurai Helmet 1": 0.0141,
    "Common Novelty Mask": 0.0147,
    "Uncommon Cowboy Hat": 0.0124,
    "Uncommon Samurai Hat 1": 0.0109,
    "Uncommon Respirator": 0.0129,
    "Uncommon Helmet 1": 0.0116,
    "Uncommon Punk Helmet 1": 0.0103,
    "Uncommon Samurai Helmet 1": 0.0109,
    "Uncommon Novelty Mask": 0.0100,
    "Rare Cowboy Hat": 0.0082,
    "Rare Samurai Hat 1": 0.0085,
    "Rare Respirator": 0.0075,
    "Rare Helmet": 0.0074,
    "Rare Punk Helmet": 0.0088,
    "Rare Samurai Helmet 1": 0.0077,
    "Rare Novelty Mask": 0.0084,
    "Epic Cowboy Hat": 0.0059,
    "Epic Samurai Hat": 0.0070,
    "Epic Respirator": 0.0068,
    "Epic Helmet": 0.0065,
    "Epic Punk Helmet": 0.0062,
    "Epic Samurai Helmet 1": 0.0066,
    "Epic Novelty Mask": 0.0048,
    "Exquisite Cowboy Hat": 0.0041,
    "Exquisite Top Hat 1": 0.0036,
    "Exquisite Samurai Hat": 0.0033,
    "Exquisite Respirator": 0.0040,
    "Exquisite Punk Helmet 1": 0.0039,
    "Exquisite Punk Helmet 2": 0.0041,
    "Exquisite Samurai Helmet 1": 0.0042,
    "Exquisite Novelty Mask": 0.0038,
    "Legendary Cowboy Hat": 0.0003,
    "Legendary Samurai Hat 1": 0.0011,
    "Legendary Helmet": 0.0008,
    "Legendary Crown": 0.0008,
    "Legendary Respirator": 0.0011,
    "Legendary Samurai Helmet 1": 0.0005,
    "Legendary Novelty Mask": 0.0007,
    "Legendary Laser Eyes": 0.0004,
    "Legendary Top Hat": 0.0009,
    "Common Top Hat 1": 0.0177,
    "Uncommon Top Hat": 0.0118,
    "Rare Top Hat": 0.0083,
    "Epic Top Hat": 0.0065,
    "Common Skull Helmet 1": 0.0160,
    "Common Skull Helmet 2": 0.0157,
    "Uncommon Skull Helmet 1": 0.0121,
    "Epic Skull Helmet 1": 0.0051,
    "Exquisite Skull Helmet 1": 0.0036,
    "Exquisite Skull Helmet 2": 0.0039,
    "Legendary Skull Helmet 1": 0.0015,
    "Legendary Skull Helmet 2": 0.0008,
    "Common Samurai Hat 2": 0.0169,
    "Uncommon Samurai Hat 2": 0.0117,
    "Rare Skull Helmet 1": 0.0080,
    "Common Skull Helmet 3": 0.0153,
    "Common Punk Helmet 2": 0.0142,
    "Common Top Hat 2": 0.0167,
    "Common Cyber Plume": 0.0198,
    "Common Punk Spikes": 0.0173,
    "Common Punk Hair": 0.0154,
    "Uncommon Skull Helmet 2": 0.0098,
    "Uncommon Punk Helmet 2": 0.0107,
    "Uncommon Helmet 2": 0.0108,
    "Uncommon Cyber Plume": 0.0125,
    "Uncommon Punk Spikes": 0.0115,
    "Uncommon Punk Hair": 0.0118,
    "Rare Skull Helmet 2": 0.0090,
    "Rare Cyber Plume": 0.0099,
    "Rare Punk Spikes": 0.0080,
    "Rare Punk Hair": 0.0101,
    "Epic Skull Helmet 2": 0.0065,
    "Epic Cyber Plume": 0.0056,
    "Epic Punk Spikes": 0.0051,
    "Epic Punk Hair": 0.0070,
    "Rare Samurai Hat 2": 0.0098,
    "Legendary Golden Hair 1": 0.0013,
    "Legendary Samurai Hat 2": 0.0013,
    "Legendary Samurai Helmet 2": 0.0008,
    "Exquisite Samurai Helmet 2": 0.0031,
    "Epic Samurai Helmet 2": 0.0057,
    "Rare Samurai Helmet 2": 0.0078,
    "Uncommon Samurai Helmet 2": 0.0116,
    "Common Samurai Helmet 2": 0.0153,
    "Mythic Cowboy Hat 1": 0.0002,
    "Mythic Cowboy Hat 2": 0.0001,
    "Mythic Cowboy Hat 3": 0.0001,
    "Mythic Cowboy Hat 4": 0.0000,
    "Mythic Cowboy Hat 5": 0.0000,
    "Mythic Cyber Plume": 0.0000,
    "Mythic Female Cowboy Hat 1": 0.0000,
    "Mythic Female Cowboy Hat 2": 0.0002,
    "Mythic Female Cowboy Hat 3": 0.0003,
    "Mythic Female Cowboy Hat 4": 0.0000,
    "Mythic Female Cowboy Hat 5": 0.0003,
    "Mythic Female Cowboy Hat 6": 0.0003,
    "Mythic Female Hair 1": 0.0002,
    "Mythic Female Hair 2": 0.0001,
    "Mythic Female Hair 3": 0.0001,
    "Mythic Female Hani Oni Mask 1": 0.0001,
    "Mythic Female Hani Oni Mask 2": 0.0001,
    "Mythic Female Hat 1": 0.0002,
    "Mythic Female Hat 2": 0.0000,
    "Mythic Female Hat 3": 0.0002,
    "Mythic Female Hat 4": 0.0000,
    "Mythic Female Mask 1": 0.0002,
    "Mythic Female Mask 2": 0.0002,
    "Mythic Female Mask 3": 0.0001,
    "Mythic Female Respirator 1": 0.0001,
    "Mythic Female Respirator 2": 0.0001,
    "Mythic Female Respirator 3": 0.0001,
    "Mythic Female Respirator 4": 0.0001,
    "Mythic Female Samurai Hat 1": 0.0000,
    "Mythic Female Samurai Hat 2": 0.0002,
    "Mythic Female Samurai Hat 3": 0.0002,
    "Mythic Female Samurai Hat 4": 0.0000,
    "Mythic Female Samurai Hat 5 (2)": 0.0002,
    "Mythic Female Samurai Hat 5": 0.0002,
    "Mythic Samurai Hat 1": 0.0001,
    "Mythic Samurai Hat 2": 0.0002,
    "Mythic Samurai Helmet 1": 0.0002,
    "Mythic Samurai Helmet 2": 0.0004,
    "Mythic Samurai Helmet 3": 0.0003,
    "Mythic Samurai Helmet 4": 0.0003,
    "Mythic Samurai Helmet 5": 0.0003,
    "Mythic Samurai Helmet 6": 0.0003,
    "Mythic Skull Helmet 1": 0.0003,
    "Mythic Skull Helmet 2": 0.0003,
    "Mythic Skull Helmet 3": 0.0002,
    "Mythic Skull Helmet 4": 0.0002,
    "Mythic Skull Helmet 5": 0.0002,
    "Mythic Skull Helmet 6": 0.0002,
    "Legendary Female Cowboy Hat": 0.0011,
    "Legendary Cyber Plume": 0.0008,
    "Legendary Punk Spikes": 0.0010,
    "Legendary Punk Hair": 0.0009,
    "Legendary Golden Hair 2": 0.0011,
    "Legendary Golden Hair 3": 0.0010,
    "Legendary Kitsune Mask 1": 0.0015,
    "Legendary Kitsune Mask 2": 0.0011,
    "Legendary Kitsune Mask 3": 0.0009,
    "Mythic Kitsune Mask 3": 0.0003,
    "Mythic Kitsune Mask 2": 0.0005,
    "Mythic Kitsune Mask 1": 0.0003,
    "Mythic Skull Helmet 7": 0.0002,
    "Mythic Skull Helmet 8": 0.0002,
    "Mythic Skull Helmet 9": 0.0003,
    "Mythic Skull Helmet 10": 0.0003,
    
    #Weapon
    "Common Cyber Sword": 0.0250,
    "Common Cyber Katana": 0.0231,
    "Common Neon Saber": 0.0222,
    "Common Chain Blade": 0.0211,
    "Common Shock Mace": 0.0219,
    "Common Light Blade": 0.0205,
    "Common Power Glove": 0.0202,
    "Uncommon Cyber Sword": 0.0143,
    "Uncommon Cyber Katana": 0.0174,
    "Uncommon Neon Saber": 0.0156,
    "Uncommon Chain Blade": 0.0156,
    "Uncommon Shock Mace": 0.0162,
    "Uncommon Sapphire Blade": 0.0155,
    "Uncommon Energy Glove": 0.0141,
    "Rare Cyber Sword": 0.0089,
    "Rare Cyber Katana 1": 0.0092,
    "Rare Neon Saber": 0.0117,
    "Rare Chain Blade": 0.0133,
    "Rare Shock Mace": 0.0113,
    "Rare Ruby Blade": 0.0100,
    "Rare Energy Glove": 0.0109,
    "Epic Cyber Sword": 0.0080,
    "Epic Amethyst Katana": 0.0086,
    "Epic Neon Saber": 0.0084,
    "Epic Chain Blade": 0.0071,
    "Epic Amethyst Mace": 0.0073,
    "Epic Amethyst Blade": 0.0069,
    "Epic Power Glove": 0.0088,
    "Exquisite Cyber Sword": 0.0046,
    "Exquisite Silver Katana": 0.0058,
    "Exquisite Neon Saber": 0.0059,
    "Exquisite Chain Blade": 0.0043,
    "Exquisite Silver Mace": 0.0032,
    "Exquisite Silver Blade": 0.0042,
    "Exquisite Power Glove": 0.0030,
    "Legendary Cyber Sword": 0.0017,
    "Legendary Gold Katana": 0.0014,
    "Legendary Neon Saber": 0.0012,
    "Legendary Chain Blade": 0.0009,
    "Legendary Gold Mace": 0.0015,
    "Legendary Gold Blade": 0.0013,
    "Legendary Power Glove": 0.0012,
    "Common Cyber Spear": 0.0222,
    "Rare Cyber Spear": 0.0116,
    "Epic Cyber Spear": 0.0078,
    "Exquisite Cyber Spear": 0.0060,
    "Legendary Cyber Spear": 0.0024,
    "Uncommon Cyber Spear": 0.0172,
    "Legendary Cyber Axe": 0.0010,
    "Exquisite Cyber Axe": 0.0044,
    "Epic Cyber Axe": 0.0100,
    "Rare Cyber Axe": 0.0126,
    "Uncommon Cyber Axe": 0.0163,
    "Common Cyber Axe": 0.0216,
    "Legendary Cyber Hammer": 0.0010,
    "Exquisite Cyber Hammer": 0.0042,
    "Epic Cyber Hammer": 0.0071,
    "Rare Cyber Hammer": 0.0132,
    "Uncommon Cyber Hammer": 0.0157,
    "Common Cyber Hammer": 0.0232,
    "Legendary Cyber Knife": 0.0008,
    "Exquisite Cyber Knife": 0.0043,
    "Epic Cyber Knife": 0.0088,
    "Rare Cyber Knife": 0.0121,
    "Uncommon Cyber Knife": 0.0156,
    "Common Cyber Knife": 0.0235,
    "Mythic Chain Blade 1": 0.0002,
    "Mythic Chain Blade 2": 0.0003,
    "Mythic Chain Blade 3": 0.0004,
    "Mythic Chain Blade 4": 0.0002,
    "Mythic Cyber Axe 1": 0.0003,
    "Mythic Cyber Axe 2": 0.0003,
    "Mythic Cyber Katana 1": 0.0002,
    "Mythic Cyber Katana 2": 0.0004,
    "Mythic Cyber Knife 1": 0.0005,
    "Mythic Cyber Knife 2": 0.0004,
    "Mythic Cyber Knife 3": 0.0004,
    "Mythic Cyber Knife 4": 0.0005,
    "Mythic Cyber Spear 1": 0.0004,
    "Mythic Cyber Spear 2": 0.0005,
    "Mythic Cyber Spear 3": 0.0007,
    "Mythic Cyber Spear 4": 0.0007,
    "Mythic Cyber Sword 1": 0.0005,
    "Mythic Cyber Sword 2": 0.0005,
    "Mythic Emerald Blade 1": 0.0006,
    "Mythic Emerald Blade 2": 0.0005,
    "Mythic Emerald Blade 3": 0.0004,
    "Mythic Emerald Blade 4": 0.0005,
    "Mythic Emerald Rose": 0.0004,
    "Legendary Gold Pistol": 0.0008,
    "Exquisite Silver Pistol": 0.0045,
    "Epic Cyber Pistol": 0.0083,
    "Uncommon Cyber Pistol": 0.0162,
    "Common Cyber Pistol": 0.0254,
    "Rare Cyber Pistol": 0.0120,
    "Legendary Gold Rose": 0.0003
}

# Default frequency for missing layers
DEFAULT_FREQUENCY = 0.5

# Trait types to check
TRAIT_TYPES = list(TRAIT_APPEARANCE_PROBABILITIES.keys())

# Function to calculate rarity score for an NFT
def calculate_rarity_score(attributes):
    total_score = 0

    for trait_type in TRAIT_TYPES:
        matching_traits = [trait for trait in attributes if trait["trait_type"] == trait_type]

        if matching_traits:
            # Trait exists, calculate rarity normally
            trait_name = matching_traits[0]["value"]
            frequency = ITEM_FREQUENCIES.get(trait_name, DEFAULT_FREQUENCY)
            rarity_score = round((1 / frequency) / SCALING_FACTOR, 2)  # Apply scaling
            matching_traits[0]["rarity_score"] = rarity_score
            matching_traits[0]["rarity_description"] = f"Appears in {round(frequency * 10000)} out of 10,000 NFTs"
        else:
            # Trait is missing, calculate its rarity based on how often it appears
            appearance_probability = TRAIT_APPEARANCE_PROBABILITIES.get(trait_type, 1)
            
            if appearance_probability == 1:
                # If 100% of NFTs have this trait, it should never be missing.
                rarity_score = 0
                rarity_description = "N/A (This trait is always present)"
            else:
                # Missing rarity score = 1 / (1 - Appearance Probability) scaled
                rarity_score = round((1 / (1 - appearance_probability)) / SCALING_FACTOR, 2)
                rarity_description = f"Does not appear in {round((1 - appearance_probability) * 100)}% of NFTs"

            # Add the missing trait to the attributes list
            attributes.append({
                "trait_type": trait_type,
                "value": "None",
                "rarity_score": rarity_score,
                "rarity_description": rarity_description
            })

        total_score += rarity_score

    return round(total_score, 2)  # Ensure proper rounding

# Function to calculate bonus
def calculate_bonus(attributes):
    tier_counts = {tier: 0 for tier in BONUS_PERCENTAGES.keys()}
    has_spirit = any("Spirit" in trait["value"] for trait in attributes)

    if has_spirit:
        return "Spirit", SPIRIT_BONUS  # **Highest Priority Bonus**

    for trait in attributes:
        trait_name = trait["value"]
        for tier in BONUS_PERCENTAGES.keys():
            if tier in trait_name:
                tier_counts[tier] += 1

    for tier, count in tier_counts.items():
        if count >= 4:
            return tier, BONUS_PERCENTAGES[tier]  # Return tier and bonus percentage
    
    return None, 0  # No bonus

# Function to calculate Cypher score
def calculate_cypher_score(rarity_score, bonus_percentage):
    base_score = rarity_score * 0.5
    bonus_contribution = base_score * bonus_percentage
    return round(base_score + bonus_contribution, 2)  # Round total Cypher score

# Update metadata files
def update_metadata():
    for folder_name in os.listdir(ROOT_DIR):
        folder_path = os.path.join(ROOT_DIR, folder_name)
        metadata_path = os.path.join(folder_path, "metadata")
        if not os.path.exists(metadata_path):
            continue

        for filename in os.listdir(metadata_path):
            if filename.endswith(".json"):
                filepath = os.path.join(metadata_path, filename)

                # Load metadata file
                with open(filepath, 'r') as file:
                    metadata = json.load(file)

                attributes = metadata.get("attributes", [])
                total_rarity_score = calculate_rarity_score(attributes)
                bonus_tier, bonus_percentage = calculate_bonus(attributes)
                total_cypher_score = calculate_cypher_score(total_rarity_score, bonus_percentage)

                # Add scores and bonus to metadata
                metadata["total_rarity_score"] = round(total_rarity_score, 2)  # Ensure rounding
                metadata["bonus"] = (
                    f"Bonus for {bonus_tier} = {round(bonus_percentage * 100, 2)}%"
                    if bonus_tier
                    else "No Bonus"
                )
                metadata["total_cypher_score"] = round(total_cypher_score, 2)  # Ensure rounding

                # Update creators field
                metadata["properties"]["creators"] = ["ETCMC"]

                # Remove compiler field
                if "compiler" in metadata:
                    del metadata["compiler"]

                # Save the updated file
                with open(filepath, 'w') as file:
                    json.dump(metadata, file, indent=4)

    print("Metadata updated successfully!")

# Run the script
update_metadata()











