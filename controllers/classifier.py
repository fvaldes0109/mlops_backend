import os
import requests
import pandas as pd
import json
from body_models import attributes as ATTRIBUTES_LIST
from llm import invoke_model

# Helper to build JSON request payload
def create_tf_serving_json(data):
    return {'inputs': {name: data[name].tolist() for name in data.keys()} if isinstance(data, dict) else data.tolist()}

# Core scoring logic
def score_model(dataset: pd.DataFrame):
    url = os.environ.get('DATABRICKS_ENDPOINT')
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

def predict(input_data):

    df = pd.DataFrame([input_data.dict()])
    
    # Encode categorical string attributes to numeric integer codes expected by the ML model
    for idx, attr_meta in enumerate(ATTRIBUTES_LIST, start=1):
        col = f'Attribute{idx}'
        if col not in df.columns:
            continue
        if attr_meta.values:
            # Create a stable mapping from the identifier (e.g. 'A11') to a zero-based integer code
            id_to_code = {val.identifier: int(val.identifier[-1]) for val in attr_meta.values}
            df[col] = df[col].map(id_to_code).fillna(-1).astype(int)
        else:
            # Ensure numerical attributes are stored as numbers (handling possible string inputs)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    result = score_model(df)
    veredict = 'Approved' if result['predictions'][0] == 1 else 'Rejected'
    
    # Map Attribute1..Attribute20 to human-readable list
    input_dict = input_data.dict()
    mapped_attributes = []
    for idx, attr_meta in enumerate(ATTRIBUTES_LIST, start=1):
        key = f"Attribute{idx}"
        raw_val = input_dict.get(key)
        if raw_val is None:
            continue
        if attr_meta.values:  # categorical, find name by identifier
            name_match = next((item.name for item in attr_meta.values if item.identifier == str(raw_val)), str(raw_val))
            mapped_attributes.append({
                'attribute': attr_meta.name,
                'value': name_match
            })
        else:
            # numerical, keep numeric value
            mapped_attributes.append({
                'attribute': attr_meta.name,
                'value': raw_val
            })

    if veredict == 'Rejected':
        llm_context = {
            'mapped_attributes': mapped_attributes
        }

        llm_output = invoke_model(llm_context)
    else:
        llm_output = None

    return {
        'veredict': veredict,
        'llm_output': llm_output
    }
