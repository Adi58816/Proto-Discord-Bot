import discord
import asyncio
import googletrans
from discord.ext import commands
from googletrans import Translator


class GoogleTransApi(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.translator = Translator()

    @commands.command()
    async def translate(self, ctx, src, dist, *args):
        text = " ".join(args)
        total = self.translator.translate(text, src=src, dest=dist).text
        await asyncio.sleep(0.3)
        await ctx.message.edit(content=total)

    @commands.command()
    async def translate_send(self, ctx, member: discord.Member, src, dist, *args):
        text = " ".join(args)
        total = self.translator.translate(text, src=src, dest=dist).text
        await ctx.channel.purge(limit=1)
        await member.send(total)

    @commands.command()
    async def translate_msg(self, ctx, src, dist, *args):
        text = " ".join(args)
        total = self.translator.translate(text, src=src, dest=dist).text
        await ctx.channel.purge(limit=1)
        await ctx.send(f"<@{ctx.author.id}> said (by translateAPI): {total}")


def setup(client):
    client.add_cog(GoogleTransApi(client))

