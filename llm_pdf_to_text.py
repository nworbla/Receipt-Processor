from pathlib import Path
import re
import os
from ollama import chat  # updated import
from tqdm import tqdm


def extract_text_from_image(image_path):

    """
    Extracts receipt data into JSON using Gemma3 4B.
    Passes the image path directly to Ollama.
    """

    # Convert to absolute path to ensure Ollama service can find it
    abs_path = str(Path(image_path).resolve())
    
    # Check if file exists before calling
    if not os.path.exists(abs_path):
        return f"{{'error': 'File not found at {abs_path}'}}"

    # Simplified, literal prompt
    prompt = """
        Analyze the attached receipt image carefully. 
        Extract the ACTUAL text from the image into JSON. 
        DO NOT make up fake data. If you cannot read a field, return null.

        Extract these specific fields:
        - store_name: The name of the business.
        - store_phone: The phone number of the store (e.g., "555-555-5555").
        - address: The full street, city, state, and zip.
        - date: Transaction date (YYYY-MM-DD).
        - time: Transaction time (HH:MM:SS).
        - total_amount: The final grand total paid (numeric).
        - items_sold_count: The total number of items purchased (usually listed at the bottom).
        - transactions: A list of objects with 'item_name' and 'price' (numeric).

        JSON Structure:
        {
        "store_name": "actual store name",
        "store_phone": "phone number",
        "address": "actual address",
        "date": "YYYY-MM-DD",
        "time": "HH:MM:SS",
        "total_amount": 0.00,
        "items_sold_count": 0,
        "transactions": [
            {"item_name": "item name", "price": 0.00}
        ]
        }
        """

    # Call the model
    response = chat(
        model='minicpm-v',
        messages=[{
            "role": "user",
            "content": prompt,
            "images": [abs_path]  # Just pass the path as a string!
        }],
        format="json",  # This forces the model to output valid JSON
        options={
        "temperature": 0,  # This makes the output deterministic and less "creative"
        "num_ctx": 2048
        }
    )

    # The `.message.content` field contains the model output
    text = response["message"]["content"]

    return text


def process_image_folder(input_folder, output_folder):
    input_p = Path(input_folder)
    output_p = Path(output_folder)
    output_p.mkdir(parents=True, exist_ok=True)

    # Get list of all PNGs in the input folder
    all_images = list(input_p.glob("*.png"))
    

    # filter out images that have already been processed
    to_process = []
    for img in all_images:
        output_file = output_p / (img.stem + ".json")
        if not output_file.exists():
            to_process.append(img)

    skipped = len(all_images) - len(to_process)
    if skipped > 0:
        print(f"Skipping {skipped} already processed receipts...")

    if not to_process:
        print("Everything is already up to date!")
        return
    
    # Add tqdm progress bar
    for image_path in tqdm(to_process, desc="Processing receipts", unit="receipt"):
        try:
            json_text = extract_text_from_image(image_path)

            output_file = output_p / (image_path.stem + ".json")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(json_text)
        except Exception as e:
            tqdm.write(f"Error processing {image_path.name}: {e}")

    print(f"\n Batch complete! Processed {len(to_process)} new receipts. Output saved to '{output_folder}'.")


# Run
process_image_folder("receipts_pngs", "texts2")