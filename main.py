import discord
import asyncio
import re
import os

# --- CONFIGURATION ---
TOKEN = os.getenv("MTU3NTMyOTgyMzIxODQ3MDk1Mg.GhVxFj.5cUa3U-tmbo54dW0zwlCG_IBotmVcs9rUlCDS4") 
ANNOUNCE_CHANNEL_ID = int(os.getenv("1551378733003448390")) # Octane's announcement channel
YOUR_COMMAND_CHANNEL_ID = int(os.getenv("1575329591046701128")) # YOUR server's #snipe-orders channel
# ---------------------

class OctaneSniper(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'â Sniper Bot is online!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # 1. Watch Octane's announcements
        if message.channel.id == ANNOUNCE_CHANNEL_ID:
            if "Limited" in message.content or "UGC Limited" in message.content:
                await self.notify_you(message)

    async def notify_you(self, message):
        # 2. Send a notification to YOUR channel
        your_channel = self.get_channel(YOUR_COMMAND_CHANNEL_ID)
        if not your_channel:
            return

        # Extract item name
        match = re.search(r'"([^"]+)"|Limited:\s*(.+)', message.content)
        if match:
            item_name = match.group(1) or match.group(2)
            
            # Send a message with a Button to Buy (if you want to go fancy)
            # Or just a simple text alert
            await your_channel.send(f"ð **NEW DROP!** {item_name}\n[Click here to view in Octane](https://octane.wtf)")

client = OctaneSniper()
client.run(TOKEN)
