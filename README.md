# Talentica_assignment_OCR
A Python-based OCR-powered invoice parser that extracts structured data into JSON format and enables intelligent querying using LLM model.



# 🧾 AI-Powered Invoice Parser with OCR, EasyOCR, and Groq Integration

This project is a lightweight AI-powered invoice parser built with **Flask**, **EasyOCR**, **Mindee API**, and **Groq (LLaMA model)**. It allows you to upload an invoice image, extract structured JSON data using OCR, and interactively query that data using a GPT-style model via Groq.

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
GROQ_API_KEY=your_groq_api_key    # Please pass the GROQ keys in key.env file.
# if your key is passkey123  >>> pass it as  >>>GROQ_API_KEY= passkey123 
```

### ▶️ 5. Run the Flask Application
```bash
python app.py
```

Now open your browser and visit:

```cpp
http://127.0.0.1:5000
```

### ▶️ 6. Application working

```
- Choose a file and click on upload
- Use the chatbot to ask any question
- click on clear to clear the dataset


```

### 🧾 Folder Structure
```bash
Talentica_assignment_OCR/
│
├── app.py                # Main Flask app
├── invoice_utils.py      # Supporting functions
├── templates/
│   └── invoice_chat.html        # Frontend HTML form
├── static/
│   └── style.css         # Optional: CSS styling
│   └── uploads/          # Consists the invoive images
│   └── invoice_data.json # JSON outputs of parsed invoices
├── requirements.txt      # Python dependencies
├── key.env               # Grok pass keys


```


### 📝 Example Use Cases
```
"What is the total amount?”
“When is the due date?”
“Who is the vendor on this invoice?”
“What is the invoice number?”

