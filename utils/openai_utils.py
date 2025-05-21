# utils/openai_utils.py
from dotenv import load_dotenv
import os
from openai import OpenAI
import requests
from fpdf import FPDF

load_dotenv()
FIGMA_TOKEN = os.getenv("FIGMA_TOKEN")
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

FIGMA_FILE_KEY = os.getenv("FIGMA_FILE_KEY")
NODE_ID = os.getenv("NODE_ID")  # Must identify this in your file

headers = {
    "X-Figma-Token": FIGMA_TOKEN,
    "Content-Type": "application/json",
}

def set_plugin_data(data_key: str, data_value: str):
    url = f"https://api.figma.com/v1/files/{FIGMA_FILE_KEY}/nodes/{NODE_ID}/plugin-data"
    payload = {data_key: data_value}
    resp = requests.put(url, headers=headers, json=payload)
    if resp.ok:
        return resp.json()
    else:
        raise Exception(f"Figma API error: {resp.text}")

# Function to generate outputs from OpenAI's API
def generate_step_output(prompt):
    
    response = client.responses.create(
        model = "o4-mini",
        reasoning = {"effort": "medium"},
        input = prompt,
    )
    
    print("Result:\n")
    print(response.output_text + "\n")
    return response.output_text


def generate_pdf_unicode(data):
    pdf = FPDF()
    pdf.add_page()

    usable_width = pdf.w - 2 * pdf.l_margin
    # Add a Unicode font (DejaVu Sans)
    pdf.add_font('DejaVu', '', 'utils/DejaVuSans.ttf', uni=True)
    
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(usable_width, 10, "Brand Strategy Summary", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font('DejaVu', '', 11)
    
    pdf.cell(usable_width, 10, f"Brand Name: {data.get('brand_name', '')}", ln=True)
    pdf.multi_cell(usable_width, 10, f"Direction: {data.get('direction', '')}", ln=True)
    pdf.ln(5)

    manifesto = data.get('manifesto', '')
    pdf.multi_cell(usable_width, 10, f"Manifesto:\n{manifesto}", ln=True)
    pdf.ln(5)

    pdf.cell(usable_width, 10, "Language Exploration:", ln=True)        
    for line in data.get('language_exploration', []):
        pdf.multi_cell(usable_width, 10, f"- {line}", ln=True)

    return bytes(pdf.output(dest='S'))  # fpdf2 expects latin1 bytes output