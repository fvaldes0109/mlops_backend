import json
import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

PROMPT = """
<system>
You are a credit risk assessor. You will be given information about a rejected credit application of a customer. This application consist of the following attributes:
- mapped_attributes: The attributes of the credit application mapped to human-readable values.
</system>

<context>
{context}
</context>

<instruction>
You must provide possible explanations on why the credit application was rejected. The reason for the veredict and advices must be based on the attributes of the credit application and not be too long, just a small paragraph. The advice must be actionable.
</instruction>
"""

def invoke_model(context: dict) -> str:
    payload = {
        "inputText": PROMPT.format(context=str(context)),
        "textGenerationConfig": {
            "maxTokenCount": 500,
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
