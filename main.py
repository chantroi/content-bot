import discord
from discord.ext import commands
from env_config import bot_token

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    bot_name = bot.user.name
    bot_id = bot.user.id
    print(f"BOT READY\n{bot_name} ({bot_id})")


bot.load_extensions("extensions")

bot.run(bot_token)
