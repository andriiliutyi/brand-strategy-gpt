# utils/file_utils.py

from PyPDF2 import PdfReader
from docx import Document

# Extract text from PDF file
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Extract text from DOCX file
def extract_docx_text(uploaded_file):
    doc = Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Extract text from TXT file
def extract_txt_text(uploaded_file):
    text = uploaded_file.getvalue().decode("utf-8")
    return text

# General function to read files (PDF, DOCX, or TXT)
def read_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_pdf_text(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_docx_text(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return extract_txt_text(uploaded_file)
    return ""
