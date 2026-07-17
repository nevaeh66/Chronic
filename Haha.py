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
DISABLE_BOT = os.getenv("DISABLE_BOT", "false").lower()

if not token:
    print("CRITICAL ERROR: DISCORD_TOKEN_HAHA is not set!")
    exit()

class MyClient(discord.Client):
    async def on_ready(self):
        # We removed the sys.exit() check from here!
        print(f'Logged on as {self.user}!')
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
                
                # --- THE DRIFT-PROOF CLOCK SYNC ---
                # Check the time AGAIN right after Discord finishes updating
                finished_time = datetime.datetime.now(tz)
                
                # Calculate exactly how many seconds are left until the next XX:XX:00
                seconds_to_sleep = 60 - finished_time.second
                
                print(f"Syncing... Sleeping for {seconds_to_sleep} seconds to hit the next minute perfectly.")
                await asyncio.sleep(seconds_to_sleep)
                
            except discord.HTTPException as e:
                if e.status == 429:
                    print("Rate limited! Taking a 5-minute break.")
                    await asyncio.sleep(20)
                else:
                    print(f"HTTP Error: {e}")
                    await asyncio.sleep(20)
            except Exception as e:
                print(f"Error in loop: {e}")
                await asyncio.sleep(20)

client = MyClient()

# --- THE CLEAN PAUSE SWITCH ---
if DISABLE_BOT == "true":
    print("DISABLE_BOT is true. The bot is paused. Exiting before login...")
    sys.exit(0)
else:
    # Only run the bot if it is NOT disabled
    client.run(token)