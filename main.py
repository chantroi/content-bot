from init import bot_token, dapi
from discord.ext import commands
import discord
import requests
import asyncio
import re
import io

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print("OK")
    
@bot.slash_command()
async def content(ctx):
    await ctx.respond("Đây là Content Download phiên bản Discord")

@bot.slash_command()
async def clear(ctx, limit: int = None):
    if limit:
        await ctx.channel.purge(limit=limit)
        message = await ctx.respond(f"Đã xoá {limit} tin nhắn trong kênh {ctx.channel.mention}")
    else:
        await ctx.channel.purge()
        message = await ctx.respond(f"Đã xoá mọi tin nhắn trong kênh {ctx.channel.mention}")
    await asyncio.sleep(10)
    await message.delete()
    
@bot.listen()
async def on_message(message):
    if any(match in message.content for match in ["tiktok", "douyin"]):
        await message.channel.trigger_typing()
        url = re.search(r"(?P<url>https?://[^\s]+)", message.content).group("url")
        r = requests.get(dapi + "/tikdou", params={"url": url}).json()
        dl_link = r.get("url")
        if isinstance(dl_link, list):
            for link in dl_link:
                bytes_data = requests.get(link).content
                file = io.BytesIO(bytes_data)
                file.name = "image.jpg"
                await message.channel.send(file=discord.File(file))
        else:
            bytes_data = requests.get(dl_link).content
            file = io.BytesIO(bytes_data)
            file.name = "video.mp4"
            await message.channel.send(file=discord.File(file))
        await message.delete()
    
bot.run(bot_token)
