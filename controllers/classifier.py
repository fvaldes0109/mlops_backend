import os
import requests
import pandas as pd
import json

# Helper to build JSON request payload
def create_tf_serving_json(data):
    return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

# Core scoring logic
def score_model(dataset: pd.DataFrame):
    url = 'https://dbc-500e84ee-bd2a.cloud.databricks.com/serving-endpoints/endpoint-1/invocations'
    headers = {
        'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}',
        'Content-Type': 'application/json'
    }

    ds_dict = {'dataframe_split': dataset.to_dict(orient='split')} if isinstance(dataset, pd.DataFrame) else create_tf_serving_json(dataset)
    data_json = json.dumps(ds_dict, allow_nan=True)
    
    response = requests.post(url, headers=headers, data=data_json)
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    
    return response.json()

# Predict function to use in FastAPI
def predict(input_data):
    df = pd.DataFrame([input_data.dict()])

    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('category')
    
    result = score_model(df)
    return result