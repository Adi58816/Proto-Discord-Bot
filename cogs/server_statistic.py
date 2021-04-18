import discord
import sqlite3
from discord.ext import commands


class Stats(commands.Cog):

    def __init__(self, client, logger):
        self.client = client
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.logger = logger

    @commands.command()
    async def s_info(self, ctx):
        embed = discord.Embed(title="SERVER INFORMATION")
        guild_id = ctx.guild.id
        guild_name = ctx.guild.name
        guild_owner = ctx.guild.owner
        embed.add_field(name="Server name:", value=f"```{guild_name}```", inline=True)
        embed.add_field(name="Server owner:", value=f"```{guild_owner}```", inline=False)
        embed.add_field(name="Amount of members:", value=f"```{ctx.guild.member_count}```")
        embed.add_field(name="Region:", value=f"```{ctx.guild.region}```")
        embed.add_field(name="Server id:", value=f"```{guild_id}```")
        embed.add_field(name=f"Categories and channels [{len(ctx.guild.categories) + len(ctx.guild.channels)}]:",
                        value=f"```Categories {len(ctx.guild.categories)} | Text: {len(ctx.guild.text_channels)} | Voice: {len(ctx.guild.voice_channels)}```",
                        inline=False)
        embed.add_field(name=f"When server was created:",
                        value=f"```{ctx.guild.created_at}```")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        self.logger.info(f"Server info was got on server {guild_id}")
        await ctx.send(embed=embed)

    @commands.command()
    async def s_stats(self, ctx):
        await ctx.send("Choose what statistic do you want to use? about (all, members, bots)")

        def check(message):
            return message.channel == ctx.channel

        msg = await self.client.wait_for("message", check=check)
        await ctx.send(f"You chose {msg.content}!")


def setup(client):
    client.add_cog(Stats(client, client.logger))
