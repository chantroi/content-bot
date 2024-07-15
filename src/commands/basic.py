from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("OK")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Bạn chưa nhập đủ tham số")

    @commands.slash_command()
    async def ping(self, ctx):
        await ctx.channel.trigger_typing()
        await ctx.respond(f"Delay: {round(self.bot.latency * 1000)}ms")

    @commands.slash_command()
    async def help(self, ctx):
        await ctx.channel.trigger_typing()
        await ctx.respond(
            f"**{self.bot.user.name}**\n"
            f"Các tính năng của **{self.bot.user.name}**\n\n"
            f"**Các tính năng:**\n"
            f"`ping` - Kiểm tra độ trễ\n"
            f"`help` - Xem thông tin bot\n"
            f"`clear` - Xoá tin nhắn trong kênh\n"
        )

    @commands.slash_command()
    async def clear(self, ctx, limit: int = None):
        await ctx.channel.trigger_typing()
        if limit:
            await ctx.channel.purge(limit=limit)
            await ctx.respond(
                f"Đã xoá {limit} tin nhắn trong kênh {ctx.channel.mention}"
            )
        else:
            await ctx.channel.purge()
            await ctx.respond(
                f"Đã xoá mọi tin nhắn trong kênh {ctx.channel.mention}", delete_after=10
            )


def setup(bot):
    bot.add_cog(Basic(bot))
