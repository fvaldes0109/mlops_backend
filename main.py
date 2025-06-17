from fastapi import FastAPI
from pydantic import BaseModel
import joblib

from controllers.update_classifier_model import update_classifier_model
from controllers.classifier import predict

app = FastAPI()
model = joblib.load("models/credit_xgb_model.pkl")

class CreditInput(BaseModel):
    Attribute1: str
    Attribute2: int
    Attribute3: str
    Attribute4: str
    Attribute5: int
    Attribute6: str
    Attribute7: str
    Attribute8: int
    Attribute9: str
    Attribute10: str
    Attribute11: int
    Attribute12: str
    Attribute13: int
    Attribute14: str
    Attribute15: str
    Attribute16: int
    Attribute17: str
    Attribute18: int
    Attribute19: str
    Attribute20: str

@app.post("/pull-classifier")
def pull_classifier():
    update_classifier_model()

@app.post("/predict")
async def predict_credit(input_data: CreditInput):
    return predict(model, input_data)
    