import os
import discord
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN_HAHA= os.getenv("DISCORD_TOKEN_HAHA")

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        # Create an 'intents' object that lets the bot see messages
        intents = discord.Intents.default()
        intents.message_content = True 
        
        # Pass that 'intents' object to the superclass
        super().__init__(*args, **kwargs, intents=intents)

# Pass the intents into your client
client = MyClient()
client.run(DISCORD_TOKEN_HAHA)