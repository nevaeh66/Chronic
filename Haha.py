import os
import discord
from dotenv import load_dotenv

load_dotenv()

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
client.run(token)