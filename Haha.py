import os
import discord
import datetime
import asyncio
import zoneinfo  # Handles the time zones correctly
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

token = os.getenv("DISCORD_TOKEN_HAHA")
if not token:
    print("CRITICAL ERROR: DISCORD_TOKEN_HAHA is not set!")
    exit()

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.loop.create_task(self.update_everything_loop())

    async def update_everything_loop(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                # Force Vancouver Time to fix the Railway AM/PM offset
                tz = zoneinfo.ZoneInfo("America/Vancouver")
                now = datetime.datetime.now(tz)
                
                current_time = now.strftime("%I:%M %p")
                status_text = f"it is {current_time}"
                bio_text = f"I keep a close watch on time: {current_time}"
                
                # Update Bio and Status
                await self.user.edit(bio=bio_text)
                activity = discord.CustomActivity(name=status_text)
                await self.change_presence(activity=activity)
                
                print(f"DEBUG: Bio and Status updated to {status_text} at {now}")
                
                # Wait until the start of the next minute to keep the clock synced
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"Error in loop: {e}")
                await asyncio.sleep(30)

                
client = MyClient()
client.run(token)