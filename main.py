from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile, Form
from Services.ServicesHandler import ServicesHandler

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return ServicesHandler().get_home()

@app.post("/api/process")
async def process(file: UploadFile = File(...), claim_id: str = Form(...)):
    return await ServicesHandler().process_pdf(file, claim_id)

