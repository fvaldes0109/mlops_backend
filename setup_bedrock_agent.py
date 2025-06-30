
import boto3
import json
import time

region = "us-east-1"
agent_name = "llmops_agent"
prompt_name = "CreditScoringPrompt"
alias_name = "prod"
version_description = "Initial production version"

bedrock = boto3.client("bedrock-agent", region_name=region)

def get_or_create_agent():
    agents = bedrock.list_agents()["agentSummaries"]
    for a in agents:
        if a["agentName"] == agent_name:
            print(f"✅ Agent exists: {a['agentId']}")
            return a["agentId"]
    print("🚀 Creating new agent...")
    response = bedrock.create_agent(
        agentName=agent_name,
        instruction="Explain credit scoring rejection reasons and suggestions.",
        foundationModel="anthropic.claude-3-sonnet-20240229-v1:0",
        idleSessionTTLInSeconds=600,
        agentResourceRoleArn="arn:aws:bedrock:us-east-1:567821811420:prompt/1KO52V09EQ:1"
    )
    return response["agent"]["agentId"]

def wait_for_prepared(agent_id):
    print("⏳ Waiting for agent to reach PREPARED status...")
    for _ in range(30):
        status = bedrock.get_agent(agentId=agent_id)["agent"]["agentStatus"]
        print("Status:", status)
        if status == "PREPARED":
            return
        time.sleep(10)
    raise Exception("❌ Agent did not reach PREPARED status in time.")

def publish_agent_version(agent_id):
    print("📦 Publishing agent version...")
    response = bedrock.prepare_agent(agentId=agent_id)
    wait_for_prepared(agent_id)
    version = bedrock.list_agent_versions(agentId=agent_id)["agentVersionSummaries"][-1]["agentVersion"]
    print(f"✅ Published version: {version}")
    return version

def create_or_update_alias(agent_id, version, alias_name):
    aliases = bedrock.list_agent_aliases(agentId=agent_id)["agentAliasSummaries"]
    for a in aliases:
        if a["agentAliasName"] == alias_name:
            print("🔁 Updating alias to new version...")
            bedrock.update_agent_alias(
                agentId=agent_id,
                agentAliasId=a["agentAliasId"],
                agentVersion=version
            )
            return a["agentAliasId"]
    print("✨ Creating alias...")
    resp = bedrock.create_agent_alias(
        agentId=agent_id,
        agentAliasName=alias_name,
        agentVersion=version
    )
    return resp["agentAliasId"]

if __name__ == "__main__":
    agent_id = get_or_create_agent()
    version = publish_agent_version(agent_id)
    alias_id = create_or_update_alias(agent_id, version, alias_name)

    print("\n✅ Setup Complete:")
    print("AGENT_ID =", agent_id)
    print("AGENT_VERSION =", version)
    print("AGENT_ALIAS_ID =", alias_id)
