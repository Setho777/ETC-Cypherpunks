import os
import json
import re

# --- Configuration ---
# Path to the folder where all metadata JSON files are stored.
metadata_dir = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA\all_metadata"
# Path to the output folder where the batch text files will be saved.
output_dir = r"C:\Users\SethM\Desktop\ETC CYPHERPUNKS\DATA\output_batches"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Regular expression to extract token ID from file name.
# Assumes file names are like "Cypherpunk-1.json"
token_id_pattern = re.compile(r'^Cypherpunk-(\d+)\.json$', re.IGNORECASE)

# List to hold eligible token IDs
eligible_tokens = []

# --- Process each metadata file ---
files = os.listdir(metadata_dir)
print(f"Found {len(files)} files in metadata directory.")

for filename in files:
    if not filename.endswith('.json'):
        continue

    match = token_id_pattern.match(filename)
    if not match:
        print(f"Skipping file (pattern not matched): {filename}")
        continue  # Skip files that don't match the expected pattern

    token_id = int(match.group(1))
    file_path = os.path.join(metadata_dir, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue

    # Use the "total_cypher_score" field from the metadata.
    # Adjust the condition as needed. Here we consider eligible if total_cypher_score is >= 10.
    try:
        score = float(data.get("total_cypher_score", 0))
    except ValueError:
        print(f"Invalid total_cypher_score in {filename}.")
        continue

    print(f"File {filename}: token {token_id} has total_cypher_score {score}")
    if score >= 10:
        eligible_tokens.append(token_id)
        print(f"Token {token_id} eligible (score >= 10)")

print(f"Total eligible tokens: {len(eligible_tokens)}")

# Optionally sort token IDs in ascending order
eligible_tokens.sort()

# --- Split eligible token IDs into batches of 100 ---
batch_size = 100
batches = [eligible_tokens[i:i + batch_size] for i in range(0, len(eligible_tokens), batch_size)]

# --- Write each batch to a separate text file ---
for index, batch in enumerate(batches, start=1):
    output_filename = f"batch_{index}.txt"
    output_file_path = os.path.join(output_dir, output_filename)
    
    # Format as a Solidity-style array literal: [id1, id2, id3, ...]
    array_literal = "[" + ",".join(str(token_id) for token_id in batch) + "]"
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            out_file.write(array_literal)
        print(f"Batch {index} written with {len(batch)} token IDs.")
    except Exception as e:
        print(f"Error writing {output_filename}: {e}")

print("Processing complete. Eligible batches saved to:", output_dir)

