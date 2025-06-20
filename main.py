from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from controllers.classifier import predict
from body_models import CreditInput, Attribute, get_attributes
from typing import List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict_credit(input_data: CreditInput):
    return predict(input_data)

@app.get("/attributes", response_model=List[Attribute])
def get_attributes_list():
    return get_attributes()

# Serve static files from the public directory
app.mount("/", StaticFiles(directory="public", html=True), name="public")