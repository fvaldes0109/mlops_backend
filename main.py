import boto3
from fastapi import FastAPI
from pydantic import BaseModel

from controllers.classifier import predict
from testaws import invoke_model

app = FastAPI()
bedrock_runtime = boto3.client('bedrock-runtime', region_name='eu-west-1')

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

@app.post("/predict")
async def predict_credit(input_data: CreditInput):
    return predict(input_data)

@app.post("/chat")
async def chat(prompt: str):
    return invoke_model(bedrock_runtime, prompt)
