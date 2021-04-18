import discord
import sqlite3
from discord.ext import commands


class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_prefix(self, ctx, new_prefix: str):
        self.cursor.execute(
            "SELECT * FROM prefixes WHERE guild_id = ?",
            (
                ctx.guild.id,
            )
        )
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute(
                "INSERT INTO prefixes VALUES(?, ?)",
                (
                    ctx.guild.id,
                    new_prefix
                )
            )
            self.connection.commit()
        else:
            self.cursor.execute(
                "UPDATE prefixes SET prefix = ? WHERE guild_id = ?",
                (
                    new_prefix,
                    ctx.guild.id
                )
            )
            self.connection.commit()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_logs(self, ctx, channel_id: int):
        guild_id = ctx.guild.id
        self.cursor.execute(
            "SELECT * FROM log_channel WHERE guild_id = ?",
            (
                guild_id,
            )
        )
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute(
                "INSERT INTO log_channel VALUES(?, ?)",
                (
                    guild_id,
                    channel_id
                )
            )
            self.connection.commit()
        else:
            self.cursor.execute(
                "UPDATE log_channel SET channel_id = ? WHERE guild_id = ?",
                (
                    channel_id,
                    guild_id
                )
            )
            self.connection.commit()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def logs_off(self, ctx):
        guild = ctx.guild
        guild_id = guild.id
        self.cursor.execute(
            "DELETE FROM log_channel WHERE guild_id = ?",
            (
                guild_id,
            )
        )
        self.connection.commit()


def setup(client):
    client.add_cog(Settings(client))
