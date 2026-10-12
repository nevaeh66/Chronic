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

# Unix Epoch origin (Jan 1, 1970) - lets Discord calculate the true live epoch hours (~497,718+)
EPOCH_START = 497117

class MyClient(discord.Client):
    async def on_ready(self):
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
                bio_text = f"I keep a close watch on time; it is currently {current_time}\n\n\nPlaying Among Us since the Unix epoch"
                
                # 1. Update Bio
                await self.user.edit(bio=bio_text)
                
                # 2. Set "Among Us" tied to Epoch 0 (displays current live epoch hours & counts up)
                game_activity = discord.Activity(
                    type=discord.ActivityType.playing,
                    name="Among Us",
                    timestamps={"start": EPOCH_START}
                )
                custom_status = discord.CustomActivity(name=status_text)
                await self.change_presence(activities=[game_activity, custom_status])
                
                print(f"DEBUG: Bio and Status updated to {status_text} at {now}")
                
                # --- THE DRIFT-PROOF CLOCK SYNC ---
                finished_time = datetime.datetime.now(tz)
                seconds_to_sleep = 60 - finished_time.second
                
                if seconds_to_sleep == 0:
                    seconds_to_sleep = 60
                
                print(f"Syncing... Sleeping for {seconds_to_sleep} seconds to hit the next minute perfectly.")
                await asyncio.sleep(seconds_to_sleep)
                
            except discord.HTTPException as e:
                if e.status == 429:
                    print("Rate limited! Taking a 5-minute break.")
                    await asyncio.sleep(300)
                else:
                    print(f"HTTP Error: {e}")
                    await asyncio.sleep(60)
            except Exception as e:
                print(f"Error in loop: {e}")
                await asyncio.sleep(60)

client = MyClient()

# --- THE CLEAN PAUSE SWITCH ---
if DISABLE_BOT == "true":
    print("DISABLE_BOT is true. The bot is paused. Exiting before login...")
    sys.exit(0)
else:
    client.run(token)