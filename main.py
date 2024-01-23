from init import bot_token, dapi
from discord.ext import commands
import discord
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print("OK")

bot.load_extensions("commands")

bot.run(bot_token)
