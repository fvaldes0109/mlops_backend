import boto3

# Create a Bedrock runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Example: Invoke Claude model from Anthropic
response = bedrock_runtime.invoke_model(
    modelId='anthropic.claude-v2',
    body=b'{"prompt": "Hello, Claude!", "max_tokens_to_sample": 100}',
    contentType='application/json',
    accept='application/json'
)

print(response['body'].read().decode())
