### IMPORTS ###
from pathlib import Path
from pdf2image import convert_from_path
from pdfminer.high_level import extract_text
import easyocr
import numpy as np


### GLOBAL VARIABLES ###
# Paths for input and output directories
PATH_INPUT = Path(".").parent.resolve()/'pdf_files'
PATH_OUTPUT = Path(".").parent.resolve()/'extracted_files'
PDF_FILES = list(PATH_INPUT.glob("*.pdf"))
                 
# OCR and text extraction settings
OCR_DPI = 300



### Functions ###

def extract_pdfminer(file_path):
    return extract_text(file_path)

def extract_ocr(file_path):
    """
    Extract text from a PDF file using OCR (Optical Character Recognition).
    """
    images = convert_from_path(file_path, dpi=OCR_DPI)
    reader = easyocr.Reader(['en'])
    images = [np.array(img) for img in images]
    result = []
    for img in images: 
        result += reader.readtext(img, detail=0, paragraph=True)

    return '\n'.join(result)

def has_valid_text_per_page(text: str) -> bool:
    """
    Check if the extracted text from each page has actual content besides just newlines.
    """
    pages = text.split('\f')  # PDF page separator in text output from PDFMiner
    for page in pages:
        page_content = page.strip()
        if len(page_content) > 0 and page_content != '\n':         # Skip empty or whitespace-only content
            return True 
    return False 


def process_pdf(pdf_file):
    """
    Process a PDF file to extract text using pdfminer first, then fall back to OCR if necessary.
    """
    print(f"Processing {pdf_file.split("/")[-1]}...")
    
    # First using pdfminer
    text_pdfminer = extract_pdfminer(pdf_file)
    if has_valid_text_per_page(text_pdfminer):
        msg = f"Valid text extracted with pdfminer for {pdf_file}"
        return text_pdfminer,msg      
    else:
        print(f"No valid text extracted with pdfminer for {pdf_file}")
    
    # Fall back to OCR extraction
    text_ocr = extract_ocr(pdf_file)
    if has_valid_text_per_page(text_ocr):
        msg = f"Valid text extracted with OCR for {pdf_file}"
        return text_ocr, msg
    
    else:
        msg = "No valid text extracted with OCR for {pdf_file}"
        return None, msg
        