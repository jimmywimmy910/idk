import discord
import requests
from discord.ext import tasks


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
