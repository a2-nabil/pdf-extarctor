import sys
import fitz  # PyMuPDF

def extract_text_and_images(pdf_path):
    results = ""
    document = fitz.open(pdf_path)

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text()
        results += f"--- Page {page_num + 1} ---\n{text}\n"

        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = f"uploads/page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)

            results += f"Saved image: {image_filename}\n"

    document.close()
    return results

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    output = extract_text_and_images(pdf_path)
    print(output)
