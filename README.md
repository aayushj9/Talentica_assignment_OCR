# Talentica_assignment_OCR
A Python-based OCR-powered invoice parser that extracts structured data into JSON format and enables intelligent querying using LLM model.



# 🧾 AI-Powered Invoice Parser with OCR, EasyOCR, and Groq Integration

This project is a lightweight AI-powered invoice parser built with **Flask**, **Tesseract**, **EasyOCR**, **Mindee API**, and **Groq (LLaMA model)**. It allows you to upload an invoice image, extract structured JSON data using OCR, and interactively query that data using a GPT-style model via Groq.

---

## 📌 Features

- Upload image-based invoices (supports PNG, JPG, JPEG, PDF, BMP, TIFF, etc.)
- Extract structured invoice data using **Tesseract** and **EasyOCR**
- JSON output is saved for each uploaded invoice
- Ask natural language questions on the invoice using **Groq's LLaMA model**
- Simple and intuitive **Flask** web UI

---



### ✅ Prerequisites

- Python 3.8+
- EasyOCR installed and added to PATH
- API Keys for:
  - [Groq](https://console.groq.com/)
- Internet connection

---
## 🚀 Getting Started

Follow these steps to set up and run the project locally.

---

### 📥 1. Clone the Repository

```bash
git clone https://github.com/aayushj9/Talentica_assignment_OCR.git
cd Talentica_assignment_OCR
```
### 🧪 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```
### 📦 3. Install Dependencies
```cpp
pip install -r requirements.txt
```
### 🔐 4. Setup API Keys
```bash
GROQ_API_KEY=your_groq_api_key
```

### ▶️ 5. Run the Flask Application
```bash
python app.py
```

Now open your browser and visit:

```cpp
http://127.0.0.1:5000
```

### 🧾 Folder Structure
```bash
Talentica_assignment_OCR/
│
├── app.py                # Main Flask app
├── templates/
│   └── index.html        # Frontend HTML form
├── static/
│   └── style.css         # Optional: CSS styling
├── uploads/              # Uploaded invoice images
├── extracted_json/       # JSON outputs of parsed invoices
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not to be shared)






```bash
git clone https://github.com/your-username/invoice-parser-ai.git
cd invoice-parser-ai'''

---

### 🧪 2. Create and Activate Virtual Environment
'''bash
Copy
Edit
# Create virtual environment
python -m venv venv

# Activate it
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate'''
📦 3. Install Dependencies
'''Install all required packages using the provided requirements.txt:

bash
Copy
Edit
pip install -r requirements.txt'''
🔐 4. Setup API Keys
'''Create a .env file in the project root with the following:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key
MINDEE_API_KEY=your_mindee_api_key
Make sure this file is not pushed to GitHub.'''

🔡 5. Install Tesseract OCR
Windows
Download from: https://github.com/UB-Mannheim/tesseract/wiki

Add the installation path to your environment variables.

macOS
bash
Copy
Edit
brew install tesseract
Ubuntu/Debian
bash
Copy
Edit
sudo apt update
sudo apt install tesseract-ocr
▶️ 6. Run the Flask Application
bash
Copy
Edit
python app.py
Visit: http://127.0.0.1:5000 in your browser.

🧾 Folder Structure
bash
Copy
Edit
invoice-parser-ai/
│
├── app.py                # Main Flask app
├── templates/
│   └── index.html        # UI page
├── static/
│   └── style.css         # CSS styles
├── uploads/              # Uploaded invoice images
├── extracted_json/       # Parsed JSON outputs
├── requirements.txt      # List of dependencies
├── .env                  # API keys (excluded from Git)
📝 Example Use Cases
“What is the total amount?”

“When is the due date?”

“Who is the vendor on this invoice?”

“What is the invoice number?”

🛑 Notes
