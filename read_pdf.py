from pypdf import PdfReader
import sys

try:
    reader = PdfReader("Historical S&P 500 Gold Data.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text)
except Exception as e:
    print(f"Error reading PDF: {e}")
