from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import requests
import pdfplumber
import uuid

app = FastAPI()

storage = {}

class URLRequest(BaseModel):
    url: str

@app.post("/process_url")
async def process_url(request: URLRequest):
    url = request.url
    response = requests.get(url)
    content = response.text 
    
    chat_id = str(uuid.uuid4())
    storage[chat_id] = {"source": "url", "content": content}
    
    return {"chat_id": chat_id, "message": "URL content processed and stored successfully."}

@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    pdf_text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text()
    
    print("Extracted PDF text:", pdf_text)
    
    chat_id = str(uuid.uuid4())
    storage[chat_id] = {"source": "pdf", "content": pdf_text}
    
    return {"chat_id": chat_id, "message": "PDF content processed and stored successfully."}


@app.get("/chat/{chat_id}")
async def chat(chat_id: str, query: str):
    if chat_id not in storage:
        return {"error": "Invalid chat_id"}
    
    content = storage[chat_id]["content"]
    
    if query.lower() in content.lower():
        return {"response": "Found relevant content"}
    else:
        return {"response": "No relevant content found"}
    
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend service hel"}
    
