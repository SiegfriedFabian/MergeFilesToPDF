import os
import io
import sys
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PyPDF2 import Transformation
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Standard width (in points)
STANDARD_WIDTH = 612  # Corresponds to the width of a letter-sized paper

def resize_pdf_page(page):
    # Create a new PDF with reportlab
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.drawString(10, 10, " ")
    c.save()
    
    # Move buffer position to the beginning
    packet.seek(0)
    
    # Read reportlab PDF into PyPDF2
    new_pdf = PdfReader(packet)
    new_page = new_pdf.pages[0]
    
    # Get original dimensions
    original_width = page.mediabox.width
    original_height = page.mediabox.height
    
    # Calculate scale and new height
    scale = STANDARD_WIDTH / original_width
    new_height = original_height * scale
    
    # Apply the scale
    page.scale_by(float(scale))
    
    # Merge the scaled page onto the blank page
    new_page.add_transformation(Transformation().translate(0, new_height - original_height))
    new_page.merge_page(page)

    return new_page

def merge_files(folder_path, output_name):
    merger = PdfMerger()
    
    # List and sort all the files in the directory
    all_files = os.listdir(folder_path)
    all_files.sort()
    
    for file_name in all_files:
        full_path = os.path.join(folder_path, file_name)
        
        if file_name.endswith('.pdf'):
            print(f'Adding PDF: {file_name}')
            pdf_reader = PdfReader(open(full_path, 'rb'))
            pdf_writer = PdfWriter()

            # Resize and add each page to the writer
            for i in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[i]
                new_page = resize_pdf_page(page)
                pdf_writer.add_page(new_page)
            
            # Save the resized PDF temporarily
            temp_pdf_path = os.path.join(folder_path, 'temp_resized_pdf.pdf')
            with open(temp_pdf_path, 'wb') as f:
                pdf_writer.write(f)
            
            # Append this PDF to the merger
            with open(temp_pdf_path, 'rb') as f:
                merger.append(f)
            
            # Remove the temporary PDF
            os.remove(temp_pdf_path)
        
        elif file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f'Adding Image: {file_name}')
            image = Image.open(full_path)
            image = image.convert('RGB')
            
            aspect_ratio = image.height / image.width
            new_height = int(STANDARD_WIDTH * aspect_ratio)

            image = image.resize((STANDARD_WIDTH, new_height))
            
            # Save the image as a PDF
            img_pdf_path = os.path.join(folder_path, 'temp_img_to_pdf.pdf')
            image.save(img_pdf_path, save_all=True)
            
            # Append this PDF to the merger
            with open(img_pdf_path, 'rb') as f:
                merger.append(f)
            
            # Remove the temporary PDF
            os.remove(img_pdf_path)
    
    # Output the merged PDF
    output_pdf_path = os.path.join('', f"{output_name}.pdf")
    with open(output_pdf_path, 'wb') as f:
        merger.write(f)
    
    print(f'Merged PDF saved as {output_pdf_path}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_files.py FOLDER NAME")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_name = sys.argv[2]

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    merge_files(folder_path, output_name)
