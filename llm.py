import boto3
import json

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

def validate_context(context: dict) -> dict:
    for key, value in context.items():
        if key.startswith("Attribute") and key[9:].isdigit():
            try:
                context[key] = int(value) if value else None
            except ValueError:
                raise ValueError(f"Invalid value for {key}: {value}")
    return context

def invoke_model(context: dict) -> str:
    full_prompt = f"""
<system>
You are a credit risk analyst. Use only the provided attributes to assess why the credit application was likely rejected. Do not assume information beyond what is given.
</system>
<context>
{json.dumps(context)}
</context>
<instruction>
Based on the mapped attributes, provide a brief explanation of why the application may have been rejected. Then, offer one clear and actionable piece of advice the applicant can follow to improve their chances of approval.
Respond in this format:
Reason: <short explanation>
Advice: <specific recommendation>
</instruction>
"""

    body = {
        "prompt": full_prompt,
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }

    response = bedrock_runtime.invoke_model(
        modelId="meta.llama3-8b-instruct-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = response["body"].read().decode()
    parsed = json.loads(result)
    return parsed.get("generation", result)