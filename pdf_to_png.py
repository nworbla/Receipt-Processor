import fitz # PyMuPDF
import os

input_folder = "receipts"
output_folder = "receipts_pngs"

# Create output folder that doesn't exist
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"): # Process only PDF files (.PDF, .pdf)
        pdf_path = os.path.join(input_folder, filename) 
        doc = fitz.open(pdf_path) # Open the PDF document

        for page_num in range(len(doc)): # Iterate through each page in the PDF
            page = doc[page_num]

            zoom = 2
            mat = fitz.Matrix(zoom, zoom)

            pix = page.get_pixmap(matrix=mat)

            output_filename = f"{os.path.splitext(filename)[0]}_page{page_num + 1}.png"
            output_path = os.path.join(output_folder, output_filename)

            pix.save(output_path)

        doc.close()

print("Done converting PDFs to PNGs.")
