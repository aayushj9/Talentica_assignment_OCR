import json
from groq import Groq

client = Groq(api_key="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")

def extract_structured_invoice_json(ocr_text: str) -> str:
    base_prompt = f"""
You are an expert in extracting structured data from noisy OCR invoice text. Given the OCR text below, extract the following fields in **strict JSON format** with these rules:
- words may vary on differnet text, plese consider order ID and order number same, also use your understading for some extent to understand such similar terms as well.
- If any value is not found, return "NA"
- Do not guess or extrapolate
- Follow the **fixed format** exactly
- Output only a valid JSON object as shown below sample — nothing else

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
      "shipping_charges" : 30,
      "tax_rate": 18,
      "tax_type" : "IGST",
      "tax_amount": 4500,
      "discount" : "NA",
      "total": 28500
    }},
    {{
      "product_name": "boAt Airdopes 141",
      "quantity": 1,
      "net_amount": 25000,
      "shipping_charges" : 30,
      "tax_rate": 18,
      "tax_type" : "IGST",
      "tax_amount": 270,
      "discount" : "NA",
      "total": 1670
    }}
  ],
  "total_summary": {{
    "total_tax": 4770,
    "discount" : 0,
    "grand_total": 30170
  }},
  "seller": {{
    "name": "Amazon Seller Services Pvt Ltd",
    "address": "8th Floor, Brigade Gateway, Dr. Rajkumar Road, Bengaluru, Karnataka - 560055",
    "gstin": "29AABCU9603R1ZM",
    "pan": "AABCU9603R",
    "cin" : "NA",
    "email": "seller-support@amazon.in"
  }}
}}

OCR Text:
\"\"\"{ocr_text}\"\"\"
"""

    def get_invoice_data(prompt):
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_completion_tokens=4000,
            top_p=0.9,
            stream=True,
        )

        response_text = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                response_text += delta.content
        return response_text

    # First attempt
    response_text = get_invoice_data(base_prompt)

    try:
        invoice_data = json.loads(response_text)
        return json.dumps(invoice_data, indent=4)
    except json.JSONDecodeError:
        retry_prompt = base_prompt + f"""

The previous response was not valid JSON. Here is the raw output received:

\"\"\"{response_text}\"\"\"

Please fix it and output **only** a valid JSON object in the exact format requested above.
"""
        response_text_retry = get_invoice_data(retry_prompt)
        try:
            invoice_data_retry = json.loads(response_text_retry)
            return json.dumps(invoice_data_retry, indent=4)
        except json.JSONDecodeError:
            return response_text_retry


# ocr_text = '''
# Tax Invoice Sold Br Tech-Connect Retuil Private Lquited Imoice unacr EELBTDC71M3 4072 shp-mn Adre4" & Ao | Jo 344l JMeLllictdm Juim #I GSTIH 29AAICAABTZDIZK 0DI1957 0783664370n0 Ordcr Doto 03 *10 Mleahbhul Putel Meahbhai Palel Venize Bungalonskar SP Rino -Venize Buraalcas Near ar Miazo ImoiceDalee Rond Rehin | Ralmctean Rnanlon Rand Rehin | Rainiceai Runanlena Wlintetnath FanlR1 PENEAD CLAlu Yend Ghilcau huns Ehilcde HATAA]DST? Anmedabjd 362331 Gularal Anmedanud 382371 Guaral CIN: US2100CL201CPICIu26j0 Pnjnt SITTTTTTT Phjne LLAAAALL Acral Item ptauici Crot Dlacout ? IALAD Ie Amounte Cal Lploc a Hanor Magic Book 15 Ryzen 47700 Do 36432 20 3557 AO 42990 00 Quad Core . 1256 GB FOMllajehhangane SSD Vldans Honie Hsnteaa4nanio Doh-WLOOHNP Thinand Liqht Laptop @umnee d_KHNP420717O07OE vst-in DCU  42990 00 16412 ?0 chs5un 42990 G0 Grand Total 42990.00 Tech Cerec Rele | Prbaleunured Aultamed Eanalon
# '''
# ocr_text = '''
# amazonin Tax InvolccIBII 0 supply Caah Nemo Origma Reidann Aaddcte Val Lkkr &h Fuxrkt Fuonns MT Suullji Indleva ochcmlniKnkTaki EfroJn Kanum;Larhmrartana ochcmlumu Kannataki ScC PAmNO: AACF 3325k Stl UT Codc: G51 Acoisertion No: 29 UCFY33254I2Y Shipolng Flicnns M S4ulljid Indb PMa Tanum_Larhmraryana ochcmlumhu Kapnatai ZFCo17 KAdailrun droly | KiRNATARA Jrdun NuitWut 203 3325714-7676307 Jice Nutbet : IN-761 Ondca Delceic70am IntolceDem Rinefenig Tee1 Involce Date 23.10.2019 75047rsr81*85*0e1il Wau KEcA Ctetnl Dal Gtut5-[6440 4447 MLa4E Ginu tuxxd Ctun TOTAL: Attlannintotd Thcuzand On Hundred And Niretv-Ire only Vamsledhi Expons Lulnorteasanmian Kter *iplyroc under re4anza cj? njin 43 Gr
# '''

# result = extract_invoice_json_from_ocr(ocr_text)
# print(result)

import json

def save_invoice_json(data, filename="invoice_data.json"):
    """
    Save the given JSON data (Python dict) into a file.

    Args:
        data (dict): Parsed JSON object.
        filename (str): File name to save the JSON.

    Returns:
        None
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Invoice JSON saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving JSON to file: {e}")

import json
import re

def clean_and_parse_json(raw_text):
    """
    Cleans input text to remove markdown code fences and 'json' label,
    then parses and returns the JSON as a Python dict.
    
    Args:
        raw_text (str): Raw text possibly containing ```json ... ``` or 'json' prefix.
        
    Returns:
        dict: Parsed JSON object.
    """
    # Remove ```json and ``` if present
    cleaned = re.sub(r'^```json\s*', '', raw_text.strip())
    cleaned = re.sub(r'```$', '', cleaned.strip())
    
    # Sometimes input might start with 'json' alone, remove it
    if cleaned.lower().startswith('json'):
        cleaned = cleaned[4:].strip()
    
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


# s = clean_and_parse_json(result)
# print(s)


def query_invoice_data_with_gpt(invoice_json: dict, question: str):
    """
    Uses Groq's LLaMA model to answer a question based on the given invoice JSON.
    
    Args:
        invoice_json (dict): The invoice data.
        question (str): The user question.

    Returns:
        str: Model's response.
    """
    #client = Groq(api_key="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")

    system_prompt = (
        "You are an assistant that answers user questions using structured invoice data provided in JSON format. "
        "If the information the user asks for is missing, null, or 'NA', respond with:\n"
        "\"Sorry, We could not find the {thing user is asking for}, please refer the image shown on right pan.\"\n"
        "Always respond in a helpful tone. Answer only from the JSON provided."
    )

    user_message = f"""Here is the invoice JSON:\n{invoice_json}\n\nQuestion: {question}"""

    # Initialize streaming response
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
            print(content, end="")  # Optional live streaming print

    return response.strip()

# question = "what is capital of india?"
# filesf = {
#     "invoice_number": "IN-761",
#     "invoice_date": "2019-10-23",
#     "order_id": "2033325714-7676307",
#     "order_date": "NA",
#     "delivery_date": "NA",
#     "invoice_type": "Tax Invoice",
#     "buyer": {
#         "name": "NA",
#         "email": "NA",
#         "phone": "NA"
#     },
#     "shipping_address": {
#         "name": "NA",
#         "address": "NA",
#         "city": "NA",
#         "state": "Karnataka",
#         "postal_code": "NA",
#         "country": "India"
#     },
#     "billing_address": {
#         "name": "NA",
#         "address": "NA",
#         "city": "NA",
#         "state": "NA",
#         "postal_code": "NA",
#         "country": "NA"
#     },
#     "items": [
#         {
#             "product_name": "NA",
#             "quantity": "NA",
#             "net_amount": "NA",
#             "shipping_charges": "NA",
#             "tax_rate": "NA",
#             "tax_type": "NA",
#             "tax_amount": "NA",
#             "discount": "NA",
#             "total": "NA"
#         }
#     ],
#     "total_summary": {
#         "total_tax": "NA",
#         "discount": "NA",
#         "grand_total": "NA"
#     },
#     "seller": {
#         "name": "Amazon Seller Services Pvt Ltd",
#         "address": "NA",
#         "gstin": "29UCFY33254I2Y",
#         "pan": "NA",
#         "cin": "NA",
#         "email": "NA"
#     }
# }


# asd = ask_invoice_question_groq(filesf,question)
# print(asd)