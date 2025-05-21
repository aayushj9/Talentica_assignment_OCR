from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import easyocr
from PIL import Image
import json
import uuid

# Import utility functions
from invoice_utils import (
    extract_structured_invoice_json,
    clean_and_parse_json,
    query_invoice_data_with_gpt
)

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
JSON_PATH = os.path.join('static', 'invoice_data.json')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    extracted_data = None

    if request.method == "POST":
        file = request.files.get("file")

        # if file and file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        if file and file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".webp", ".heic", ".heif")):
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # OCR using EasyOCR
            image = Image.open(file_path)
            reader = easyocr.Reader(['en'])
            ocr_results = reader.readtext(image)
            ocr_text = " ".join([detection[1] for detection in ocr_results])
            print(" Raw OCR text extrcted")

            # Extract structured data
            raw_json_text = extract_structured_invoice_json(ocr_text)
            print("OCR text filtered")

            extracted_data = clean_and_parse_json(raw_json_text)
            print("Converted to JSON format")

            # Save structured data to file
            with open(JSON_PATH, "w") as f:
                json.dump(extracted_data, f, indent=4)

            image_url = file_path

    elif request.method == "GET" and os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r") as f:
            extracted_data = json.load(f)

        # Display the latest uploaded image
        files = os.listdir(UPLOAD_FOLDER)
        if files:
            image_url = os.path.join(UPLOAD_FOLDER, files[0])

    return render_template("invoice_chat.html", image_url=image_url, extracted_data=extracted_data)


@app.route("/clear", methods=["POST"])
def clear_files():
    # Delete all uploaded images
    for filename in os.listdir(UPLOAD_FOLDER):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")

    # Delete the JSON data
    if os.path.exists(JSON_PATH):
        try:
            os.remove(JSON_PATH)
        except Exception as e:
            print(f"Error deleting JSON file: {e}")

    return redirect(url_for("index"))


@app.route("/chat", methods=["POST"])
def chat():
    question = request.form.get("message", "")
    
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    answer = query_invoice_data_with_gpt(data, question)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
