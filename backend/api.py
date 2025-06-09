from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .process_pdf import process_pdf  # Assuming process_pdf.py is in the same directory
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend folder at root
frontend_path = Path(__file__).parent.parent / "frontend"
@app.get("/")
def serve_frontend():
    return FileResponse(frontend_path / "index.html")

@app.post("/extract-pdf/")
async def extract_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    os.makedirs("processed", exist_ok=True)
    app.mount("/processed", StaticFiles(directory="processed"), name="processed")
    
    pdf_path = f"processed/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(contents)

    # Simulated extraction — replace with your logic
    text,msg = process_pdf(pdf_path)
    if text is None:
        return JSONResponse(status_code=500, content={"error": msg})
    txt_path = f"processed/{file.filename.split(".")[0]}.txt"
    with open(txt_path, "w") as f:
        f.write(text)

    return JSONResponse({
        "filename": file.filename,
        "message": msg,
        "output_txt": txt_path,
        "text_preview": text[:300]
    })
