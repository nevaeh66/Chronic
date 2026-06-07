import os
import discord
from dotenv import load_dotenv
print(f"DEBUG: I am looking for the token in: {os.environ.get('DISCORD_TOKEN_HAHA')}")
raw_token = os.getenv("DISCORD_TOKEN_HAHA")
DISCORD_TOKEN_HAHA = raw_token.strip() if raw_token else None

# DEBUG: Check if the token is actually there
token = os.getenv("DISCORD_TOKEN_HAHA")
if not token:
    print("CRITICAL ERROR: DISCORD_TOKEN_HAHA is not set!")
else:
    print(f"Token found! Length: {len(token)}") 

class MyClient(discord.Client):
    # Remove the 'intents' argument from here
    def __init__(self, *args, **kwargs):
        # Remove the 'intents=intents' from super().__init__
        super().__init__(*args, **kwargs)

# Remove the 'intents=discord.Intents.default()' argument here
client = MyClient() 
client.run(token)