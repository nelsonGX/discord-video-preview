import discord
import os
from dotenv import load_dotenv
import re
import random

from download_video import download_video
from generate import create_gif_preview

load_dotenv()

async def check_url(message_content):
    url_regex = r"(?x)(?:https?:)?(?:\/\/)?(?:www\.)?(?:(?:youtube\.com\/(?:watch\?v=|embed\/|v\/)|youtu\.be\/)(?P<youtube_id>[\w-]{11})|(?:instagram\.com\/(?:reel|reels)\/(?P<instagram_id>[\w-]{11})))(?:[\/?&]\S*)?"
    url_match = re.search(url_regex, message_content)
    if url_match:
        url = url_match.group(1)
        print(f"URL detected: {url}")
        return url
    return False

async def generate_uuid():
    uuid_string = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
    return uuid_string

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    url = await check_url(message.content)
    if url:
        uuid = await generate_uuid()
        print(f"Downloading video from URL: {url}")
        await download_video(url, uuid)
        print(f"Creating GIF preview for video: {uuid}.mp4")
        await create_gif_preview(f"tmepvid_{uuid}.mp4", f"tmepvid_{uuid}.gif")
        print(f"Uploading GIF preview: {uuid}.gif")
        reply_msg = await message.reply(file=discord.File(f"tmepvid_{uuid}.gif"), mention_author=False)
        await reply_msg.add_reaction("❌")
        print(f"Cleaning up files: {uuid}")
        os.remove(f"tmepvid_{uuid}.mp4")
        os.remove(f"tmepvid_{uuid}.gif")

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    
    if reaction.emoji == "❌":
        await reaction.message.delete()

client.run(os.getenv("DISCORD_TOKEN"))