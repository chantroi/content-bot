from typing import Optional

import discord
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.slash_command()
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(f"Delay: {round(self.bot.latency * 1000)}ms")

    @commands.slash_command()
    async def clear(
        self, ctx: discord.ApplicationContext, limit: Optional[int] = None
    ) -> None:
        if limit:
            await ctx.channel.purge(limit=limit)
            await ctx.respond(
                f"Đã xoá {limit} tin nhắn trong kênh {ctx.channel.mention}",
                delete_after=10,
            )
        else:
            await ctx.channel.purge()
            await ctx.respond(
                f"Đã xoá tất cả tin nhắn trong kênh {ctx.channel.mention}",
                delete_after=10,
            )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Basic(bot))
