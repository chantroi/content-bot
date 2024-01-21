from discord.ext import commands
from init import bot_token
import discord

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(
    description="Content Download",
    intents=intents,)

@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")

@bot.user_command(name="Say Hello")
async def hi(ctx, user):
    await ctx.respond(f"{ctx.author.mention} says hello to {user.name}!")
   
@bot.event
async def on_ready():
    await bot.load_extensions("commands.basic")
bot.run(bot_token)