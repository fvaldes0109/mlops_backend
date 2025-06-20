import json

def invoke_model(bedrock_runtime, prompt: str, max_token_count: int) -> str:
    payload = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": max_token_count,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    response = bedrock_runtime.invoke_model(
        modelId='amazon.titan-text-lite-v1',
        body=json.dumps(payload).encode('utf-8'),
        contentType='application/json',
        accept='application/json'
    )

    return response['body'].read().decode()
