import os
import discord
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN_HAHA= os.getenv("DISCORD_TOKEN_HAHA")
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This dictionary stores a separate history for every person
        self.memories = {}

# Pass the intents into your client
client = MyClient()
client.run(DISCORD_TOKEN_HAHA)