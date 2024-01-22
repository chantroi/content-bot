from init import bot_token
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print("OK")

bot.load_extensions("commands")
bot.run(bot_token)