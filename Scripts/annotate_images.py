import os
from PIL import Image, ImageDraw, ImageFont
import json

# Base directory for processing
BASE_DIR = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA"

# Font settings
FONT_PATH = r"C:\Windows\Fonts\Impact.TTF"  # Custom font path
FONT_SIZE = 26.5  # Font size

# Default text and outline colors
DEFAULT_TEXT_COLOR = (0, 153, 51)  # Darker Green (Main Text)
DEFAULT_OUTLINE_COLOR = (255, 223, 0)  # Yellow (Outline)
OUTLINE_THICKNESS = 2  # Outline thickness

# Special colors for Mythic Background
MYTHIC_TEXT_COLOR = (0, 153, 51)  # Dark Green
MYTHIC_OUTLINE_COLOR = (173, 255, 47)  # Light Lime Green

# Text positioning offsets
RARITY_X_OFFSET = -200  # Horizontal offset for total rarity score
RARITY_Y_OFFSET = -90  # Vertical offset for total rarity score
CYPHER_X_OFFSET = 200   # Horizontal offset for total cypher score
CYPHER_Y_OFFSET = -90  # Vertical offset for total cypher score

# Function to draw outlined text
def draw_outlined_text(draw, position, text, font, inner_color, outline_color, outline_thickness):
    x, y = position
    # Draw the outline
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    
    # Draw the main text
    draw.text((x, y), text, font=font, fill=inner_color)

# Function to overlay scores on an image
def annotate_image(image_path, total_rarity_score, total_cypher_score, is_mythic):
    try:
        # Open the image
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)

            # Load the font
            try:
                font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
            except IOError:
                print(f"Font not found at {FONT_PATH}. Using default font.")
                font = ImageFont.load_default()

            # Text to overlay
            rarity_text = f"Rarity Score: {total_rarity_score}"
            cypher_text = f"Cypher Score: {total_cypher_score}"

            # Get image dimensions
            image_width, image_height = img.size

            # Calculate rarity text position
            rarity_width, rarity_height = draw.textbbox((0, 0), rarity_text, font=font)[2:]
            rarity_x = (image_width // 2) + RARITY_X_OFFSET - (rarity_width // 2)
            rarity_y = image_height + RARITY_Y_OFFSET - (rarity_height // 2)

            # Calculate cypher text position
            cypher_width, cypher_height = draw.textbbox((0, 0), cypher_text, font=font)[2:]
            cypher_x = (image_width // 2) + CYPHER_X_OFFSET - (cypher_width // 2)
            cypher_y = image_height + CYPHER_Y_OFFSET - (cypher_height // 2)

            # Determine colors based on background rarity
            if is_mythic:
                text_color = MYTHIC_TEXT_COLOR
                outline_color = MYTHIC_OUTLINE_COLOR
            else:
                text_color = DEFAULT_TEXT_COLOR
                outline_color = DEFAULT_OUTLINE_COLOR

            # Draw outlined text
            draw_outlined_text(draw, (rarity_x, rarity_y), rarity_text, font, text_color, outline_color, OUTLINE_THICKNESS)
            draw_outlined_text(draw, (cypher_x, cypher_y), cypher_text, font, text_color, outline_color, OUTLINE_THICKNESS)

            # Save the modified image
            img.save(image_path)
            print(f"Annotated image updated: {image_path}")
    except Exception as e:
        print(f"Failed to annotate image {image_path}: {e}")

# Main function to process all nested directories
def process_data_directories():
    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)
        if os.path.isdir(folder_path):
            images_path = os.path.join(folder_path, "images")
            metadata_path = os.path.join(folder_path, "metadata")

            if not os.path.exists(images_path) or not os.path.exists(metadata_path):
                print(f"Skipping folder {folder_path}: Missing 'images' or 'metadata' directory.")
                continue

            for metadata_file in os.listdir(metadata_path):
                if metadata_file.endswith(".json"):
                    metadata_file_path = os.path.join(metadata_path, metadata_file)

                    # Read the metadata file
                    with open(metadata_file_path, 'r') as file:
                        metadata = json.load(file)

                    # Extract scores
                    total_rarity_score = metadata.get("total_rarity_score", "N/A")
                    total_cypher_score = metadata.get("total_cypher_score", "N/A")

                    # Check if the background is Mythic
                    attributes = metadata.get("attributes", [])
                    is_mythic = any(attr.get("trait_type") == "Background" and "Mythic" in attr.get("value", "") for attr in attributes)

                    # Find the corresponding image
                    image_filename = metadata.get("image", "")
                    image_file_path = os.path.join(images_path, image_filename)

                    if not os.path.exists(image_file_path):
                        print(f"Image file not found: {image_file_path}")
                        continue

                    # Annotate the image
                    annotate_image(image_file_path, total_rarity_score, total_cypher_score, is_mythic)

# Run the script
if __name__ == "__main__":
    process_data_directories()












