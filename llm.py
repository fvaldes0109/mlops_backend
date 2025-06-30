import boto3
import json
import os
from botocore.exceptions import ClientError

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
bedrock_agent = boto3.client("bedrock-agent", region_name="us-east-1")

# --- Function: Load Prompt Text from Prompt Management ---
def load_prompt_text(prompt_id: str, version_number: str = "6", fallback_file: str = "prompt_template.txt") -> str:
    try:
        client = boto3.client("bedrock-agent", region_name="us-east-1")
        response = client.get_prompt(
            promptIdentifier=f"prompt/{prompt_id}:{version_number}"
        )
        prompt_text = response["prompt"]["content"]

        # ✅ Save to file
        with open(fallback_file, "w", encoding="utf-8") as f:
            f.write(prompt_text)

        print(f"✅ Loaded from Bedrock + saved to {fallback_file}")
        return prompt_text

    except ClientError as e:
        print(f"⚠️ Failed to load from Bedrock: {e}")
        print(f"🔁 Loading from fallback file: {fallback_file}")

        if not os.path.exists(fallback_file):
            raise FileNotFoundError(f"Fallback prompt file not found: {fallback_file}")

        with open(fallback_file, "r", encoding="utf-8") as f:
            return f.read()
        
# --- Optional: Validate context input ---
def validate_context(context: dict) -> dict:
    for key, value in context.items():
        if key.startswith("Attribute") and key[9:].isdigit():
            try:
                context[key] = int(value) if value else None
            except ValueError:
                raise ValueError(f"Invalid value for {key}: {value}")
    return context

def load_prompt_text_from_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# --- Main function to call LLM ---
def invoke_model(context: dict) -> str:
    # prompt_template = load_prompt_text("1KO52V09EQ", "DRAFT")
    # full_prompt = prompt_template.format(context=json.dumps(context))

    prompt_template = load_prompt_text("1KO52V09EQ", "DRAFT", "prompt_template.txt")
    full_prompt = prompt_template.format(context=json.dumps(context))

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