import os
import discord
from dotenv import load_dotenv

raw_token = os.getenv("DISCORD_TOKEN_HAHA")
DISCORD_TOKEN_HAHA = raw_token.strip() if raw_token else None

# DEBUG: Check if the token is actually there
token = os.getenv("DISCORD_TOKEN_HAHA")
if not token:
    print("CRITICAL ERROR: DISCORD_TOKEN_HAHA is not set!")
else:
    print(f"Token found! Length: {len(token)}") 

class MyClient(discord.Client):
    # ... (your existing class code) ...
    
    # Let's add this to see if it even connects
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

client = MyClient(intents=discord.Intents.default()) # Make sure you handle intents properly
try:
    client.run(token)
except Exception as e:
    print(f"Bot crashed with error: {e}")