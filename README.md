# PDF2Text

A FastAPI-based web application for extracting text from PDF files, with automatic OCR fallback for scanned documents. The project features a REST API for PDF uploads, a simple frontend for easy interaction, and organized input/output directories. Dependencies are managed with [Poetry](https://python-poetry.org/).

---

## Project Structure

```
.
├── backend/
│   ├── api.py            # FastAPI app (API endpoints, frontend mounting)
│   ├── process_pdf.py    # PDF processing and text extraction logic
│   └── ...
├── frontend/
│   └── index.html        # Frontend HTML interface (file upload and result display)
├── pdf_files/            # Directory for incoming PDF files (input)
├── processed/            # Directory for processed files (.txt outputs, etc.)
├── pyproject.toml        # Poetry project configuration
├── README.md
├── .gitignore
...
```

---

## Features

- **Web Interface:** Upload PDFs from your browser and see extracted results instantly.
- **PDF Upload API:** Upload PDFs via a REST API endpoint.
- **Text Extraction:** Uses `pdfminer.six` for extracting text from PDFs.
- **OCR Fallback:** Falls back to OCR (`easyocr` + `pdf2image`) if standard extraction fails.
- **Organized Storage:** Input PDFs in `/pdf_files/`, processed text in `/processed/`.
- **Text Preview and Download Info:** See a preview of extracted text and the path to the saved file.

---

## Getting Started

### 1. Install [Poetry](https://python-poetry.org/docs/#installation)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install Dependencies

From the project root:

```bash
poetry install
```

### 3. Run the Backend API

```bash
poetry run uvicorn backend.api:app --reload
```

---

## Using the Web Interface

1. Open `frontend/index.html` in your web browser.
2. Click **Choose File** and select a PDF.
3. Click **Upload & Extract**.
4. The result will show:
    - **Processed:** Filename of your PDF
    - **Saved to:** Path where the extracted text was saved (e.g., `processed/yourfile.txt`)
    - **Preview:** The first portion of the extracted text

---

## API Usage (for developers)

- **Endpoint:** `POST /extract-pdf/`
- **Form field:** `file` (the PDF file)

**Example using `curl`:**
```bash
curl -F "file=@path/to/yourfile.pdf" http://localhost:8000/extract-pdf/
```

**Response Example:**
```json
{
  "filename": "yourfile.pdf",
  "message": "Valid text extracted with pdfminer for processed/yourfile.pdf",
  "output_txt": "processed/yourfile.txt",
  "text_preview": "First 300 characters of extracted text..."
}
```

---

## How it Works

1. User selects a PDF through the browser or sends it to the API.
2. The backend saves the file to `/pdf_files/` and tries to extract text with `pdfminer.six`.
3. If extraction fails, it uses OCR (`easyocr`/`pdf2image`).
4. Extracted text is saved to `/processed/<filename>.txt` and the result is shown in the browser (filename, output path, and preview).

---

## Notes

- **Poppler** is required for `pdf2image`.  
  See [pdf2image installation instructions](https://github.com/Belval/pdf2image#how-to-install).
- **Large PDFs:** OCR may be slow for big or image-heavy files.
- **Permissions:** Ensure the app has write access to `/processed/` and `/pdf_files/`.

---

## License

MIT License

---

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
- [easyocr](https://github.com/JaidedAI/EasyOCR)
- [pdf2image](https://github.com/Belval/pdf2image)