import os
import discord
import datetime
import asyncio
from dotenv import load_dotenv

# Load the environment variables from the .env file in the current directory
load_dotenv()

# Get the token
token = os.getenv("DISCORD_TOKEN_HAHA")
if not token:
    print("CRITICAL ERROR: DISCORD_TOKEN_HAHA is not set!")
    exit() # Stop the script if no token is found

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # Start the background task
        self.loop.create_task(self.update_everything_loop())

    async def update_everything_loop(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                # Strictly wait 60 seconds, but start at your offset
                # This ensures the loop triggers exactly every minute
                await asyncio.sleep(1) 
                
                # Perform the update
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                status_text = f"it is {current_time}"
                
                # Update Bio
                await self.user.edit(bio=status_text)
                
                # Update Status
                activity = discord.CustomActivity(name=status_text)
                await self.change_presence(activity=activity)
                
                print(f"DEBUG: Bio and Status updated to {status_text}")
                
            except Exception as e:
                print(f"Error in loop: {e}")
                await asyncio.sleep(1)

# Run the client
client = MyClient()
client.run(token)