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
                # 1. Get current system time
                now = datetime.datetime.now()
                
                # 2. Format the time
                current_time = now.strftime("%I:%M %p")
                status_text = f"it is {current_time}"
                bio_text = f"I keep a close watch on time: {current_time}"
                
                # 3. Update Bio and Status
                await self.user.edit(bio=bio_text)
                activity = discord.CustomActivity(name=status_text)
                await self.change_presence(activity=activity)
                
                print(f"DEBUG: Bio and Status updated to {status_text} at {now}")
                
                # 4. SLEEP UNTIL THE START OF THE NEXT MINUTE
                # This kills the 'drift' because it always resets to the clock
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"Error in loop: {e}")
                await asyncio.sleep(60) # Only sleep 60 on error
# Run the client
client = MyClient()
client.run(token)