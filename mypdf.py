import fitz  # PyMuPDF

def extract_text_and_images(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)

    # Iterate through each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)  # Load the page
        text = page.get_text()  # Extract text
        print(f"--- Page {page_num + 1} ---")
        print(text)  # Print extracted text

        # Extract images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]  # XREF of the image
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]  # Get the image bytes
            image_ext = base_image["ext"]  # Get the image extension

            # Save the image
            image_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
            print(f"Saved image: {image_filename}")

    # Close the document
    document.close()

# Replace 'your_pdf_file.pdf' with the path to your PDF
extract_text_and_images('hero.pdf')
