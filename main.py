import boto3
from fastapi import FastAPI

from controllers.classifier import predict
from testaws import invoke_model
from body_models import ChatInput, CreditInput, Attribute, get_attributes
from typing import List

app = FastAPI()
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict_credit(input_data: CreditInput):
    return predict(input_data)

@app.post("/chat")
async def chat(input_data: ChatInput):
    return invoke_model(bedrock_runtime, input_data.prompt, input_data.max_token_count)

@app.get("/attributes", response_model=List[Attribute])
def get_attributes_list():
    return get_attributes()