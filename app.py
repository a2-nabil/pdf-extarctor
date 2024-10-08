from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_images_and_text():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['pdf']
    pdf_path = os.path.join('uploads', pdf_file.filename)
    pdf_file.save(pdf_path)

    document = fitz.open(pdf_path)
    output_data = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text()  # Extract text
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = f"extracted_image_{page_num + 1}_{img_index + 1}.{image_ext}"
            image_filepath = os.path.join('static', image_filename)
            with open(image_filepath, "wb") as image_file:
                image_file.write(image_bytes)

            output_data.append({'img_src': f"/static/{image_filename}", 'text': text})

    document.close()
    return jsonify(output_data)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)
