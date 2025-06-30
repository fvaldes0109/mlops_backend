import boto3

client = boto3.client("bedrock-agent", region_name="us-east-1")

# 1. Create Prompt (Draft)
create_resp = client.create_prompt(
    name="CreditScoringExplanation",
    description="Explain credit rejection reasons and suggestions.",
    variants=[
        {
            "name": "v1",
            "modelId": "meta.llama3-8b-instruct-v1:0",
            "templateType": "TEXT",
            "inferenceConfiguration": {
                "text": { "temperature": 0.5 }
            },
            "templateConfiguration": {
                "text": {
                    "text": """<system>
You are a credit analyst. Based only on the input below, explain:

- Reason 1:
- Reason 2:
- Suggestion:
</system>

<context>
{{context}}
</context>"""
                }
            }
        }
    ]
)

prompt_id = create_resp["id"]

# 2. Version the Prompt
version_resp = client.create_prompt_version(promptIdentifier=prompt_id)
print("✅ Prompt ARN:", version_resp["arn"])