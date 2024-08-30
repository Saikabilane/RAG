import os
import fitz
import csv
from PIL import Image

# Open the PDF file
pdf_file = fitz.open("./anatomy_vol_3_edited_final.pdf")

# Get the number of pages
pg_nums = len(pdf_file)

# List to hold image objects
images = []

# List to hold image filenames
image_filenames = []

# Extract images from each page
for pg_num in range(pg_nums):
    page = pdf_file[pg_num]
    images.extend(page.get_images())

if len(images) == 0:
    raise ValueError("No images found")

for i, image in enumerate(images, start=1):
    xref = image[0]
    base_image = pdf_file.extract_image(xref)
    image_bytes = base_image['image']
    image_ext = base_image['ext']
    image_name = 'image'+str(i)+'.'+image_ext
    
    # Save image file
    with open(os.path.join('./images/', image_name), 'wb') as image_file:
        image_file.write(image_bytes)
    
    # Save image name to the list
    image_filenames.append(image_name)
