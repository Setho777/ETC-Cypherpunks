from PIL import Image
import os
import base64
import json

# Configuration
input_folder = r"C:\Users\SethM\Desktop\TEST FOLDER\images"
output_folder = r"C:\Users\SethM\Desktop\TestOutput"
base64_output_folder = r"C:\Users\SethM\Desktop\TestOutput\Base64"
metadata_folder = r"C:\Users\SethM\Desktop\TEST FOLDER\metadata"
final_metadata_folder = r"C:\Users\SethM\Desktop\TestOutput\FinalMetadata"
final_base64_metadata_folder = r"C:\Users\SethM\Desktop\TestOutput\FinalBase64Metadata"
final_hex_metadata_folder = r"C:\Users\SethM\Desktop\TestOutput\FinalHexMetadata"

# **🔥 STRONGER IMAGE COMPRESSION SETTINGS**
target_size_kb = 40  # **Lower image size even further**
min_quality = 10  # **Allow compression down to lowest quality if needed**
hex_metadata_limit_kb = 120  # **Only HEX metadata must stay below 120KB**

# Ensure output folders exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(base64_output_folder, exist_ok=True)
os.makedirs(final_metadata_folder, exist_ok=True)
os.makedirs(final_base64_metadata_folder, exist_ok=True)
os.makedirs(final_hex_metadata_folder, exist_ok=True)

# Function to compress images **AGGRESSIVELY**
def compress_image(input_path, output_path, target_size_kb):
    img = Image.open(input_path).convert("RGB")
    quality = 70  # **Start with low quality**

    while quality >= min_quality:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        if os.path.getsize(output_path) <= target_size_kb * 1024:
            break  
        quality -= 5  # **Lower quality more if needed**

# Process all images
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        base_name = filename.replace(".png", "")
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, base_name + ".jpg")
        base64_output_path = os.path.join(base64_output_folder, base_name + ".txt")
        metadata_path = os.path.join(metadata_folder, base_name + ".json")
        final_metadata_path = os.path.join(final_metadata_folder, base_name + ".json")
        final_base64_metadata_path = os.path.join(final_base64_metadata_folder, base_name + ".txt")
        final_hex_metadata_path = os.path.join(final_hex_metadata_folder, base_name + ".txt")

        # **🚀 Stronger compression on images**
        compress_image(input_path, output_path, target_size_kb)

        # **Base64 encode compressed image**
        with open(output_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")

        # **Save Base64 image separately**
        with open(base64_output_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(base64_image)

        # **Check if metadata exists**
        if not os.path.exists(metadata_path):
            print(f"⚠️ Missing metadata for {filename}, skipping.")
            continue

        # **Read JSON metadata safely**
        if os.path.getsize(metadata_path) == 0:
            print(f"⚠️ Warning: {filename} metadata is empty. Skipping.")
            continue
        try:
            with open(metadata_path, "r", encoding="utf-8") as metadata_file:
                metadata = json.load(metadata_file)
        except json.JSONDecodeError:
            print(f"❌ Error: {filename} contains invalid JSON. Skipping.")
            continue

        # **🔥 AGGRESSIVELY REMOVE UNNECESSARY METADATA**
        metadata = {
            "n": metadata.get("name", ""),  # "name" → "n"
            "d": "ETC Cypherpunks",  # **🔥 Super short description**
            "s": metadata.get("total_cypher_score", 0),  # "total_cypher_score" → "s"
            "image": f"data:image/jpeg;base64,{base64_image}",
            "attributes": [{"t": attr["trait_type"], "v": attr["value"]}
                           for attr in metadata.get("attributes", [])]
        }

        # **🔥 Convert JSON to Minified Format Before Encoding**
        metadata_json = json.dumps(metadata, separators=(",", ":"))  
        base64_metadata = base64.b64encode(metadata_json.encode("utf-8")).decode("utf-8")
        hex_metadata = metadata_json.encode("utf-8").hex()  

        # **Save Minified JSON**
        with open(final_metadata_path, "w", encoding="utf-8") as output_file:
            json.dump(metadata, output_file, separators=(",", ":"))

        # **Save Base64 metadata**
        with open(final_base64_metadata_path, "w", encoding="utf-8") as base64_metadata_file:
            base64_metadata_file.write(base64_metadata)

        # **Save HEX metadata (for on-chain inscription)**
        with open(final_hex_metadata_path, "w", encoding="utf-8") as hex_metadata_file:
            hex_metadata_file.write(hex_metadata)

        # **🔥 Calculate Sizes**
        hex_size_kb = len(hex_metadata) / 1024  # **Only HEX metadata matters**
        image_size_kb = os.path.getsize(output_path) / 1024  # Image size (for info)

        # **Print results**
        print(f"{filename} → Compressed: {image_size_kb:.2f} KB, HEX Metadata: {hex_size_kb:.2f} KB")

        if hex_size_kb > hex_metadata_limit_kb:
            print(f"❌ {filename} is STILL TOO LARGE! Further compression needed.")
        else:
            print(f"✅ {filename} fits within the 120 KB ETC limit!")

print("✅ Compression, encoding, and metadata optimization complete.")
print(f"✅ Base64 image data saved in: {base64_output_folder}")
print(f"✅ Final metadata saved in: {final_metadata_folder}")
print(f"✅ HEX metadata for inscription saved in: {final_hex_metadata_folder}")











