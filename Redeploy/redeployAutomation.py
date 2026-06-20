import os
import requests

# Pulling credentials from the Railway environment variables
RAILWAY_TOKEN = os.getenv("f9c2d95f-3644-4373-ab3f-0a4d920df42c")
SERVICE_ID = os.getenv("a0c6028b-5fdb-434f-8580-3c986c601947")
ENV_ID = os.getenv("1e434460-e790-43f0-95c3-a3d8219a9aa5")

def force_reboot():
    url = "https://backboard.railway.app/graphql/v2"
    
    headers = {
        "Authorization": f"Bearer {RAILWAY_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Railway's internal GraphQL mutation to trigger a redeploy
    query = """
    mutation serviceInstanceRedeploy($environmentId: String!, $serviceId: String!) {
      serviceInstanceRedeploy(environmentId: $environmentId, serviceId: $serviceId)
    }
    """
    
    variables = {
        "environmentId": ENV_ID,
        "serviceId": SERVICE_ID
    }
    
    print(f"Targeting Service: {SERVICE_ID}...")
    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
    
    if response.status_code == 200:
        print("Success! The target service is now redeploying.")
    else:
        print(f"CRITICAL ERROR {response.status_code}: {response.text}")

if __name__ == "__main__":
    if not RAILWAY_TOKEN or not SERVICE_ID or not ENV_ID:
        print("Missing environment variables. Check your Railway settings.")
        exit(1)
        
    force_reboot()