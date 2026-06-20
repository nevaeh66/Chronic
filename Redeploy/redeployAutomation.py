import os
import requests

# Pulling credentials from the Railway environment variables
RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN")
SERVICE_ID = os.getenv("TARGET_SERVICE_ID")
ENV_ID = os.getenv("TARGET_ENV_ID")

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