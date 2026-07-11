import os
import discord
import datetime
import asyncio
import zoneinfo
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

token = os.getenv("DISCORD_TOKEN_HAHA")
# This is the "Pause Switch" variable
DISABLE_BOT = os.getenv("DISABLE_BOT", "false").lower()

if not token:
    print("CRITICAL ERROR: DISCORD_TOKEN_HAHA is not set!")
    exit()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        # Check the Pause Switch immediately upon startup
        if DISABLE_BOT == "true":
            print("DISABLE_BOT is true. The bot is pausing itself. Exiting...")
            await self.close()
            sys.exit(0)
            
        self.loop.create_task(self.update_everything_loop())

    async def update_everything_loop(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                tz = zoneinfo.ZoneInfo("America/Vancouver")
                now = datetime.datetime.now(tz)
                
                current_time = now.strftime("%I:%M %p")
                status_text = f"it is {current_time}"
                bio_text = f"I keep a close watch on time; it is currently {current_time}"
                
                await self.user.edit(bio=bio_text)
                activity = discord.CustomActivity(name=status_text)
                await self.change_presence(activity=activity)
                
                print(f"DEBUG: Bio and Status updated to {status_text} at {now}")
                
                # INCREASED SLEEP TO 60 SECONDS TO PREVENT 429 ERRORS
                await asyncio.sleep(60)
                
            except discord.HTTPException as e:
                if e.status == 429:
                    print("Rate limited! Taking a 5-minute break.")
                    await asyncio.sleep(300)
                else:
                    print(f"HTTP Error: {e}")
                    await asyncio.sleep(60)
            except Exception as e:
                print(f"Error in loop: {e}")
                await asyncio.sleep(20)

client = MyClient()
client.run(token)

