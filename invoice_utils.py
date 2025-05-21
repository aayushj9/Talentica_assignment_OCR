import json
import re
from groq import Groq

#client = Groq(api_key="***********")

import json
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv(dotenv_path="key.env")
# Get the API key
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def extract_structured_invoice_json(ocr_text: str) -> str:
    base_prompt = f"""
You are an expert in extracting structured data from noisy OCR invoice text. Given the OCR text below, extract the following fields in **strict JSON format** with these rules:
- Treat terms like "order number" and "order ID" as the same.
- If any value is not found, return "NA"
- Do not guess or extrapolate
- Follow the exact format shown
- Return only a valid JSON object. No explanations.

Expected format:
{{
  "invoice_number": "INVOICE/2025/12345",
  "invoice_date" : "2025-01-01",
  "order_id": "403-1122334-5566778",
  "order_date": "2025-01-01",
  "delivery_date": "2025-01-01",
  "invoice_type": "Tax Invoice",
  "buyer": {{
    "name": "Rahul Sharma",
    "email": "rahul.sharma@example.com",
    "phone": "+91-9876543210"
  }},
  "shipping_address": {{
    "name": "Rahul Sharma",
    "address": "Flat No. 12B, Sunrise Apartments",
    "city": "Bengaluru",
    "state": "Karnataka",
    "postal_code": "560001",
    "country": "India"
  }},
  "billing_address": {{
    "name": "Rahul Sharma",
    "address": "Flat No. 12B, Sunrise Apartments",
    "city": "Bengaluru",
    "state": "Karnataka",
    "postal_code": "560001",
    "country": "India"
  }},
  "items": [
    {{
      "product_name": "Apple Watch SE",
      "quantity": 1,
      "net_amount": 25000,
      "shipping_charges": 30,
      "tax_rate": 18,
      "tax_type": "IGST",
      "tax_amount": 4500,
      "discount": "NA",
      "total": 28500
    }}
  ],
  "total_summary": {{
    "total_tax": 4500,
    "discount": 0,
    "grand_total": 28500
  }},
  "seller": {{
    "name": "Amazon Seller Services Pvt Ltd",
    "address": "8th Floor, Brigade Gateway, Dr. Rajkumar Road, Bengaluru, Karnataka - 560055",
    "gstin": "29AABCU9603R1ZM",
    "pan": "AABCU9603R",
    "cin": "NA",
    "email": "seller-support@amazon.in"
  }}
}}

OCR Text:
\"\"\"{ocr_text}\"\"\"
"""

    def get_response(prompt):
        response_text = ""
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_completion_tokens=4000,
            top_p=0.9,
            stream=True,
        )
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                response_text += delta.content
        return response_text

    response_text = get_response(base_prompt)
    try:
        return json.dumps(json.loads(response_text), indent=4)
    except json.JSONDecodeError:
        retry_prompt = base_prompt + f"""
The previous response was not valid JSON. Here is the response received:
\"\"\"{response_text}\"\"\"

Please correct and return only valid JSON as specified.
"""
        response_retry = get_response(retry_prompt)
        try:
            return json.dumps(json.loads(response_retry), indent=4)
        except json.JSONDecodeError:
            return response_retry



def clean_and_parse_json(raw_text: str):
    cleaned = re.sub(r'^```json\s*', '', raw_text.strip())
    cleaned = re.sub(r'```$', '', cleaned.strip())
    if cleaned.lower().startswith('json'):
        cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def query_invoice_data_with_gpt(invoice_json: dict, question: str) -> str:
    system_prompt = (
        "You are an assistant that answers user questions using the provided structured invoice JSON. "
        "If any field is missing, null, or marked 'NA', respond with:\n"
        "\"Sorry, we could not find the {thing user is asking for}, please refer the image shown on right pan.\""
    )

    user_message = f"Here is the invoice JSON:\n{invoice_json}\n\nQuestion: {question}"

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        top_p=1,
        stream=True,
        max_completion_tokens=512,
    )

    response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            response += content
            print(content, end="")  # Live stream response

    return response.strip()
