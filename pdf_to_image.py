from pdf2image import convert_from_path
import os

print("Script started")

input_folder = "receipts"
output_folder = "images"

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.endswith(".pdf"):
        print(f"Converting {file}")
        images = convert_from_path(os.path.join(input_folder, file), dpi=300)

        for i, img in enumerate(images):
            output_path = os.path.join(output_folder, f"{file[:-4]}_{i}.png")
            img.save(output_path, "PNG")