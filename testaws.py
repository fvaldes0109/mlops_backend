def invoke_model(bedrock_runtime, prompt: str) -> str:
    response = bedrock_runtime.invoke_model(
        modelId='anthropic.claude-v2',
        body=b'{"prompt": "' + prompt + '", "max_tokens_to_sample": 100}',
        contentType='application/json',
        accept='application/json'
    )

    return response['body'].read().decode()
