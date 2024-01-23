from init import bot_token, dapi
import discord
import requests
import re # Thêm thư viện re để sử dụng biểu thức chính quy

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("OK")
    
@bot.slash_command()
async def content(ctx): # Bỏ tham số self vì hàm này không phải là một phương thức của lớp bot
    await ctx.respond("Đây là Content Download phiên bản Discord")
    
@bot.listen()
async def on_message(message):
    if any(match in message.content for match in ["tiktok", "douyin"]):
        await message.channel.trigger_typing() # Sử dụng message.channel.trigger_typing() thay vì ctx.typing()
        url = re.search(r"(?P<url>https?://[^\s]+)", message.content) # Tìm url trong nội dung tin nhắn
        if url: # Kiểm tra xem có url nào được tìm thấy hay không
            url = url.group("url") # Lấy giá trị của url
            r = requests.get(dapi + "/tikdou", params={"url": url}).json()
            dl_link = r.get("url")
            if isinstance(dl_link, list):
                for link in dl_link:
                    await message.channel.send(file=discord.File(link)) # Sử dụng message.channel.send() thay vì ctx.send()
            else:
                await message.channel.send(file=discord.File(dl_link))
            await message.delete() # Sử dụng message.delete() thay vì ctx.message.delete()
    
bot.run(bot_token)
