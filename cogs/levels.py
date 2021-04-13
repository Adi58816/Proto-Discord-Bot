# importing discord py
import discord
import sqlite3
from discord.ext import commands


# levelsystem class
class LevelSystem(commands.Cog):

    # init function
    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect(
            "database.db"
        )
        self.cursor = self.conn.cursor()

    # messages listenting
    @commands.Cog.listener()
    async def on_message(self, msg):
        msg_author = msg.author

        if msg_author == self.client.user:
            return

        msg_guild = msg.guild
        length = len(msg.content)

        self.cursor.execute(
            "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
            (
                msg_guild.id,
                msg_author.id
            )
        )
        data = self.cursor.fetchone()

        if data == None:
            self.cursor.execute(
            "INSERT INTO server_activity VALUES (?, ?, 0, 0)",
                (
                    msg_guild.id,
                    msg_author.id
                )
            )
            await msg.channel.send(
                f"{msg_author.mention} This is your first message on this server"
            )
            self.conn.commit()
            return

        current_server_activity = data[2]
        current_server_level = data[3]

        current_server_activity += length
        new_server_level = int(
            current_server_activity / 2000
        )

        if (new_server_level != current_server_level):
            await msg.channel.send(
                f"{msg_author.mention} You got new {new_server_level} level on this server!"
            )

        self.cursor.execute(
            "UPDATE server_activity SET user_server_activity = ?, user_level = ? WHERE guild_id = ? AND member_id = ?",
            (
                current_server_activity,
                new_server_level,
                msg_guild.id,
                msg_author.id
            )
        )
        self.conn.commit()

    @commands.command()
    async def level(self, ctx):
        msg_author = ctx.message.author

        msg_guild = ctx.guild
        self.cursor.execute(
            "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
            (
                msg_guild.id,
                msg_author.id
            )
        )
        data = self.cursor.fetchone()
        if data == None:
            await ctx.send(
                "You have 0 LEVEL on the server!"
            )
            return
        else:
            await ctx.send(
                f"You have {data[3]} level on the server!"
            )

    @commands.command()
    async def activity_to_moneys(self, ctx, levels: int):
        msg_author = ctx.message.author
        length = len(ctx.message.content)
        msg_guild = ctx.guild
        self.cursor.execute(
            "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
            (
                msg_guild.id,
                msg_author.id
            )
        )
        data = self.cursor.fetchone()
        if (data[3] < levels):
            await ctx.send(
                "You don't have this amount of levels"
            )
        else:
            self.cursor.execute(
                "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
                (
                    msg_guild.id,
                    msg_author.id
                )
            )
            data = self.cursor.fetchone()
            current_server_activity = data[2]
            current_server_level = data[3]
            current_server_activity -= levels * 2000
            new_server_level = current_server_level - levels
            self.cursor.execute(
                "UPDATE server_activity SET user_server_activity = ?, user_level = ? WHERE guild_id = ? AND member_id = ?",
                (
                    current_server_activity,
                    new_server_level,
                    msg_guild.id,
                    msg_author.id
                )
            )
            self.conn.commit()
            user_data = self.get_user_data(msg_author, ctx.guild)
            server = ctx.guild
            self.cursor.execute(
			    "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[3] + (levels ** 3) * 1000,
                    msg_author.id,
                    server.id
                )
		    )
            self.conn.commit()
            await ctx.send(
                f"You got {(levels ** 2) * 1000} 💸. (Level ^ 3 * 1000)"
            )
    

    def get_user_data(self, member, server):
        self.cursor.execute(
			"SELECT * FROM economic WHERE member_id = ? AND guild_id = ?",
            (
                member.id,
                server.id
            )
		)
        data = self.cursor.fetchone()
        if data is None:
            self.cursor.execute(
				"INSERT INTO economic VALUES (?, ?, 0, 0)",
                (
                    server.id,
                    member.id
                )
			)
            self.conn.commit()
            data = self.cursor.fetchone()
            return (
                server.id, 
                member.id, 
                0, 
                0
            )
        return data


def setup(client):
    client.add_cog(LevelSystem(client))
