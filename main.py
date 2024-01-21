import discord, os
from discord.ext import commands
from init import bot_token

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

bot.run(bot_token)