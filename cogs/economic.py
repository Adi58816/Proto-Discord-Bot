import sqlite3
import asyncio
import os
import sys
from loguru import logger
import discord
from discord.ext import commands
from discord.utils import get


class EconomyCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    @commands.command()
    async def bal(self, ctx):
        """
        :param ctx:
        :return:
        """
        data = self.get_user_data(
            ctx.message.author,
            ctx.guild
        )
        embed = discord.Embed(
            title="Users' balance",
            description=f"User: {ctx.message.author.mention}",
            color=0x00AAFF
        )
        embed.set_thumbnail(
            url=ctx.message.author.avatar_url
        )
        embed.add_field(
            name="Server",
            value=ctx.guild.name
        )
        embed.add_field(
            name="Wallet",
            value=f"{data[3]} 💸"
        )
        embed.add_field(
            name="Bank",
            value=f"{data[2]} 💰"
        )
        await ctx.send(
            embed=embed
        )

    @commands.command()
    async def gbal(self, ctx, member: discord.Member):
        """
        :param ctx:
        :param member:
        :return:
        """
        data = self.get_user_data(member, ctx.guild)
        embed = discord.Embed(
            title="Users' balance",
            description=f"User: {member.mention}",
            color=0x00AAFF)
        embed.set_thumbnail(
            url=member.avatar_url
        )
        embed.add_field(
            name="Server",
            value=ctx.guild.name
        )
        embed.add_field(
            name="Wallet",
            value=f"{data[3]} 💸"
        )
        embed.add_field(
            name="Bank", value=f"{data[2]} 💰"
        )
        await ctx.send(
            embed=embed
        )

    @commands.has_permissions(
        administrator=True
    )
    @commands.command()
    async def set_wallet(self, ctx, member: discord.Member, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        server = ctx.guild
        self.cursor.execute(
            "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
            (
                balance,
                member.id,
                server.id
            )
        )
        self.conn.commit()

    @commands.has_permissions(
        administrator=True
    )
    @commands.command()
    async def add_bal(self, ctx, member: discord.Member, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        user_data = self.get_user_data(
            member,
            ctx.guild
        )
        server = ctx.guild
        self.cursor.execute(
            "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
            (
                int(user_data[3]) + int(balance),
                member.id,
                server.id
            )
        )
        self.conn.commit()

    @commands.command()
    async def send_gift(self, ctx, member: discord.Member, cash: int):
        """
        :param ctx:
        :param member:
        :param cash:
        :return:
        """
        user_data = self.get_user_data(
            ctx.message.author,
            ctx.guild
        )
        getter_balance = int(
            self.get_user_data(
                member,
                ctx.guild
            )[3]
        )
        users_balance = int(
            user_data[3]
        )
        if int(cash) > users_balance:
            await ctx.send(
                f"{ctx.message.author.mention} You don't have so much moneys!"
            )
        else:
            self.cursor.execute(
                "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    users_balance - int(cash),
                    ctx.message.author.id,
                    ctx.guild.id
                )
            )
            self.cursor.execute(
                "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    getter_balance + int(cash),
                    member.id,
                    ctx.guild.id
                )
            )
            self.conn.commit()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def del_bal(self, ctx, member: discord.Member, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        user_data = self.get_user_data(
            member,
            ctx.guild
        )
        server = ctx.guild
        if user_data[3] < int(balance):
            await ctx.send(
                f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}"
            )
        else:
            self.cursor.execute(
                "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[3] - int(balance),
                    member.id,
                    server.id
                )
            )
            self.conn.commit()

    @commands.command()
    async def to_bank(self, ctx, balance: int):
        """
        :param ctx:
        :param balance:
        :return:
        """
        member = ctx.message.author
        user_data = self.get_user_data(member, ctx.guild)
        server = ctx.guild
        if user_data[3] < int(balance):
            await ctx.send(
                f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}")
            return
        else:
            self.cursor.execute(
                "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[3] - int(balance),
                    member.id,
                    server.id
                )
            )
            self.cursor.execute(
                "UPDATE economic SET bank_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[2] + int(balance),
                    member.id,
                    server.id
                )

            )
            self.conn.commit()

    @commands.command()
    async def from_bank(self, ctx, balance: int):
        """
        :param ctx:
        :param balance:
        :return:
        """
        member = ctx.message.author
        user_data = self.get_user_data(member, ctx.guild)
        server = ctx.guild
        if user_data[2] < int(balance):
            await ctx.send(
                f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}"
            )
            return
        else:
            self.cursor.execute(
                "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[3] + int(balance),
                    member.id,
                    server.id
                )
            )
            self.cursor.execute(
                "UPDATE economic SET bank_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[2] - int(balance),
                    member.id,
                    server.id
                )
            )
            self.conn.commit()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def add_shop_item(self, ctx, role: discord.Role, prise: int, *description):
        """
        :param description:
        :param ctx:
        :param role:
        :param prise:
        :return:
        """
        description = " ".join(description)
        self.cursor.execute(
            "INSERT INTO economic_shop_item VALUES(?, ?, ?, ?)",
            (
                ctx.guild.id,
                role.id,
                prise,
                description
            )
        )
        self.conn.commit()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def del_shop_item(self, ctx, role: discord.Role):
        """
        :param ctx:
        :param role:
        :return:
        """
        self.cursor.execute(
            "DELETE FROM economic_shop_item WHERE guild_id = ? AND role_id = ?",
            (
                ctx.guild.id,
                role.id,
            )
        )
        self.conn.commit()

    def get_user_data(self, member, server):
        """
        :param member:
        :param server:
        :return:
        """
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
            return server.id, member.id, 0, 0
        return data

    @commands.command()
    async def shop(self, ctx):
        """
        :param ctx:
        :return:
        """
        self.cursor.execute(
            "SELECT * FROM economic_shop_item WHERE guild_id = ? ORDER BY prise",
            (
                ctx.guild.id,
            )
        )
        data = self.cursor.fetchall()
        data.reverse()
        embed = discord.Embed(title="SHOP")
        for item in data:
            embed.add_field(name=f"Role: {ctx.guild.get_role(item[1]).name}", value=f"Prise: {item[2]}\nDescription: {item[3]}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, role: discord.Role):
        """
        :param ctx:
        :param role:
        :return:
        """
        self.cursor.execute(
            "SELECT * FROM economic_shop_item WHERE guild_id = ?",
            (
                ctx.guild.id,
            )
        )
        data = self.cursor.fetchall()
        role_exists = False
        balance = 0
        for item in data:
            if item[1] == role.id:
                role_exists = True
                balance = item[2]
                break

        if not role_exists:
            await ctx.send("This role is not in SHOP!")
        else:
            user_data = self.get_user_data(ctx.message.author, ctx.guild)
            server = ctx.guild
            if user_data[3] < int(balance):
                await ctx.send(
                    f"{ctx.message.author.mention} You can't buy role {role.mention}"
                    f", cause you don't have this amount of money!")
            else:
                self.cursor.execute(
                    "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                    (
                        user_data[3] - int(balance),
                        ctx.message.author.id,
                        server.id
                    )
                )
                self.conn.commit()
                try:
                    await ctx.message.author.add_roles(role)
                    await ctx.send(f"You got role {role.mention}. Thank you for paying!")
                except:
                    await ctx.send(
                        f"{ctx.message.author.mention} Bot is not adminstrator, so he can't add roles to users :(")

    @commands.command()
    async def add_voice_to_money(self, ctx, id, moneys_per_minute):
        """
        :param ctx:
        :param id:
        :param moneys_per_minute:
        :return:
        """
        self.cursor.execute(
            "SELECT * FROM `moneys_for_voice_activity` WHERE guild_id = ? AND channel_id = ?",
            (
                ctx.guild.id,
                id
            )
        )
        data = self.cursor.fetchone()
        if data is not None:
            await ctx.send(
                "This channel is already exists in the database! To update values you can just type "
                "```/delete_voice_to_money (voice channel id)``` and then execute this command again")
        else:
            self.cursor.execute(
                "INSERT INTO `moneys_for_voice_activity` VALUES(?, ?, ?)",
                (
                    ctx.guild.id,
                    id,
                    moneys_per_minute
                )
            )
            self.connection.commit()

    @commands.command()
    async def delete_voice_to_money(self, ctx, id):
        """
        :param ctx:
        :param id:
        :return:
        """
        self.cursor.execute(
            "DELETE FROM `moneys_for_voice_activity` WHERE guild_id = ? AND channel_id = ?",
            (
                ctx.guild.id,
                id
            )
        )
        self.connection.commit()


# setup function
def setup(client):
    """
    :param client:
    :return:
    """
    client.add_cog(EconomyCog(client))
