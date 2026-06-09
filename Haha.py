import os
import discord
import datetime
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

    async def update_everything_loop(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                status_text = f"it is {current_time}"
                
                # 1. Update the PUBLIC BIO
                await self.user.edit(bio=status_text)
                
                # 2. Update the PUBLIC CUSTOM STATUS
                # This makes the "chronic" text change to the time
                activity = discord.CustomActivity(name=status_text)
                await self.change_presence(activity=activity)
                
                print(f"DEBUG: Bio and Status updated to {status_text}")
            except Exception as e:
                print(f"Error: {e}")

# Remove the 'intents=discord.Intents.default()' argument here
client = MyClient() 
client.run(token)