import discord
import re
import os
import sys

# --- CONFIGURATION ---
# These keys MUST match exactly what you typed in Render's Environment Variables section
TOKEN = os.getenv("DISCORD_TOKEN") 
ANNOUNCE_CHANNEL_ID = int(os.getenv("ANNOUNCE_CHANNEL_ID")) 
YOUR_CHANNEL_ID = int(os.getenv("YOUR_CHANNEL_ID")) 
# ---------------------

class OctaneSniper(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print('✅ Sniper Bot is online! Waiting for drops...')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Watch Octane's announcement channel
        if message.channel.id == ANNOUNCE_CHANNEL_ID:
            if "Limited" in message.content or "UGC Limited" in message.content:
                await self.notify(message)

    async def notify(self, message):
        target_channel = self.get_channel(YOUR_CHANNEL_ID)
        if not target_channel:
            return

        match = re.search(r'"([^"]+)"|Limited:\s*(.+)', message.content)
        if match:
            item_name = match.group(1) or match.group(2)
            await target_channel.send(f"🚀 **NEW DROP!** {item_name}\n[Click here to buy](https://octane.wtf)")

if __name__ == "__main__":
    client = OctaneSniper()
    client.run(TOKEN)
