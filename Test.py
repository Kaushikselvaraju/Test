from flask import Flask, request, jsonify
import PyPDF2
import os

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and file.filename.lower().endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            extracted_text = ''
            for page in pdf_reader.pages:
                extracted_text += page.extract_text() or ''

            return jsonify({'text': extracted_text.strip()})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file format. Only PDF files are supported.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
