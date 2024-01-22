from init import bot_token
import discord
import os

dapi = os.getenv("DETA_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("OK")
    
@bot.slash_command()
async def content(self, ctx):
    await ctx.respond("Đây là Content Download phiên bản Discord")
    
@bot.listen
async def ttdy(ctx):
    await ctx.typing()
    url = re.search(r"(?P<url>https?://[^\s]+)", ctx.message.content).group("url")
    r = requests.get(dapi + "/tikdou", params={"url": url}).json()
    dl_link = r.get("url")
    if isinstance(dl_link, list):
        for link in dl_link:
            await ctx.send(file=discord.File(link))
    else:
        await ctx.send(file=discord.File(dl_link))
    await ctx.message.delete()
    
bot.run(bot_token)