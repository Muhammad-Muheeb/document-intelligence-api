from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from pypdf import PdfReader
from app.ai_service import analyze_cv_text
from app.database import init_db, save_analysis, list_analyses

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

init_db()

@app.get("/")
def home():
       return FileResponse("static/index.html")


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    reader = PdfReader(file_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

    return {
        "filename": file.filename,
        "status": "uploaded",
        "extracted_text": extracted_text
    }


@app.post("/documents/analyze")
async def analyze_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    reader = PdfReader(file_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

    if not extracted_text.strip():
        raise HTTPException(status_code=422, detail="No text found in this PDF")

    try:
        result = analyze_cv_text(extracted_text)
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error))

    try:
        analysis_id = save_analysis(file.filename, result)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Database error: {error}")

    return {
        "id": analysis_id,
        "filename": file.filename,
        "analysis": result
    }


@app.get("/documents")
async def get_documents():
    return list_analyses()