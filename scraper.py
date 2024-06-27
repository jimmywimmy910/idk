import discord
import requests
from discord.ext import tasks

# Replace with your actual values
TOKEN = 'MTA5NTcwOTA2MzQ2NTE1MjU5Mw.Gk62Nc.xnkmp6cPFRjHRIsnGOIOmP31IrwPl80nIw7Q5U'
CHANNEL_ID = 1252764057652428861  # Replace with your channel ID
NEOCITIES_API_KEY = '9b7a1c8b2adcfc713062f2143d671da0'

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    fetch_links.start()

@tasks.loop(minutes=10)
async def fetch_links():
    channel = client.get_channel(CHANNEL_ID)
    messages = await channel.history(limit=15).flatten()
    roblox_links = [msg.content for msg in messages if 'roblox.com' in msg.content]
    upload_links(roblox_links)

def upload_links(links):
    if not links:
        return
    links_content = '\n'.join(links).encode('utf-8')
    response = requests.post(
        'https://neocities.org/api/upload',
        headers={
            'Authorization': f'Bearer {NEOCITIES_API_KEY}'
        },
        files={
            'links.txt': ('links.txt', links_content)
        }
    )
    print(response.json())

client.run(TOKEN)
