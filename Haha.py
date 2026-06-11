import os
import discord
import datetime
import asyncio
import zoneinfo
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
        # Gatekeepers to prevent loop duplication on reconnects
        self.loop_started = False
        self.typing_started = False

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        # Start the Time loop
        if not self.loop_started:
            self.loop.create_task(self.update_everything_loop())
            self.loop_started = True

        # Start the Global Typing loop
        if not self.typing_started:
            self.loop.create_task(self.global_dm_typing_loop())
            self.typing_started = True

    async def update_everything_loop(self):
        await self.wait_until_ready()
        
        while not self.is_closed():
            try:
                # Force Vancouver Time to fix the Railway AM/PM offset
                tz = zoneinfo.ZoneInfo("America/Vancouver")
                now = datetime.datetime.now(tz)
                
                current_time = now.strftime("%I:%M %p")
                status_text = f"it is {current_time}"
                bio_text = f"I keep a close watch on time; it is currently {current_time}"
                
                # Update Bio and Status
                await self.user.edit(bio=bio_text)
                activity = discord.CustomActivity(name=status_text)
                await self.change_presence(activity=activity)
                
                print(f"DEBUG: Bio and Status updated to {status_text} at {now}")
                
                # Kept at 60s to prevent an instant Captcha lock on the time updates
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Error in time loop: {e}")
                await asyncio.sleep(60)

    async def global_dm_typing_loop(self):
        await self.wait_until_ready()
        print("DEBUG: Global DM typing loop started.")
        
        while not self.is_closed():
            try:
                # Loop through every private channel the bot has currently cached
                for channel in self.private_channels:
                    if isinstance(channel, (discord.DMChannel, discord.GroupChannel)):
                        try:
                            await channel.typing()
                            # 1.5s delay spaces out the requests enough to mostly avoid 429s
                            await asyncio.sleep(1.5) 
                        except discord.HTTPException as http_err:
                            # The Emergency Brake: Catch the rate limit before it crashes the loop
                            if http_err.status == 429:
                                print(f"DEBUG: Rate limit hit on channel {channel.id}. Cooling down for 15s...")
                                await asyncio.sleep(15)
                            else:
                                print(f"HTTP Error: {http_err}")
                        except Exception as e:
                            print(f"Unexpected error on channel {channel.id}: {e}")
                
                # Wait before starting the next sweep to let the API breathe
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"Fatal error in master typing loop: {e}")
                await asyncio.sleep(10)

client = MyClient()
client.run(token)