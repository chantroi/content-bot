import discord
from discord.ext import commands
from env_config import bot_token

intents: discord.Intents = discord.Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(intents=intents)


@bot.event
async def on_ready() -> None:
    bot_name: str = bot.user.name
    bot_id: int = bot.user.id
    print(f"BOT READY\n{bot_name} ({bot_id})")


bot.load_extensions("cogs")

bot.run(bot_token)
