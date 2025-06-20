import json
import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

PROMPT = """<system>
You are a credit risk analyst. Use only the provided attributes to assess why the credit application was likely rejected. Do not assume information beyond what is given.
</system>

<context>
{context}
</context>

<instruction>
Based on the mapped attributes, provide a brief explanation of why the application may have been rejected. Then, offer one clear and actionable piece of advice the applicant can follow to improve their chances of approval.

Respond in this format:
Reason: <short explanation>
Advice: <specific recommendation>
</instruction>"""

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
