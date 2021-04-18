# importing modules
import discord
import requests
import random
import io
import json
import sqlite3
import asyncio
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from datetime import datetime


class MiningCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prises = {
            "rtx 3090": "3293000",
            "6900 xt": "2415000",
            "rtx 3080": "2735000",
            "6800 xt": "1679000",
            "rtx 3070": "1679000",
            "rtx 2080 ti": "1644000",
            "rtx a6000": "686000",
        }
        self.moneys_ = {
            "rtx 3090": "10932102",
            "6900 xt": "1023503",
            "rtx 3080": "9839210",
            "6800 xt": "933221",
            "rtx 3070": "872129",
            "rtx 2080 ti": "522342",
            "rtx a6000": "421242",
        }
        self.chances_to_broke = [
            12, 22, 18, 24, 41, 55, 65
        ]
        self.videocards_companies = [
            "NVidia", "AMD", "NVidia", "AMD", "NVidia", "NVidia", "NVidia"
        ]
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    @commands.command()
    async def m_info(self, ctx):
        await ctx.send(
            file=discord.File(fp="video_card_ferm_2.png")
        )

    @commands.command()
    async def m_buy(self, ctx, *videocard_words):
        videocard = " ".join(videocard_words)
        if not (videocard in list(self.prises.keys())):
            await ctx.send("This videocard doesn NOT exists!")
        else:
            user_data = self.get_user_data(
                ctx.message.author,
                ctx.guild
            )
            wallet = user_data[3]
            member = ctx.message.author
            server = ctx.guild
            prise = int(self.prises[videocard])

            if (prise > wallet):
                await ctx.send("You don't have this amount of moneys!")
            else:
                self.add_videocard(videocard, server, member)
                self.cursor.execute(
                    "UPDATE `economic` SET `wallet_balance` = ? WHERE `member_id` = ? AND `guild_id` = ?",
                    (
                        (user_data[3] - int(prise)),
                        member.id,
                        server.id
                    )
                )
            self.connection.commit()

    @commands.command()
    async def m_my_farm(self, ctx):
        self.cursor.execute(
            "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
            (
                ctx.guild.id,
                ctx.message.author.id
            )
        )
        result = self.cursor.fetchall()
        embed = discord.Embed(
            title=f"{ctx.message.author.name}'s cryptofarm!",
            description=f"Farm for mining crypto coins!",
            color=0x00AAFF
        )
        embed.set_thumbnail(
            url=ctx.message.author.avatar_url
        )
        for element in result:
            embed.add_field(
                name=f"{element[2].title()} videocards:",
                value=f"Amount: {element[3]}\nManufacturer: {self.videocards_companies[list(self.prises.keys()).index(element[2])]}"
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def m_end(self, ctx):
        self.cursor.execute("DELETE FROM  is_mining WHERE guild_id = ? AND member_id = ?",
                            (
                                ctx.guild.id,
                                ctx.message.author.id)
                            )
        self.cursor.execute("INSERT INTO is_mining VALUES (?, ?, 0)",
                            (
                                ctx.guild.id,
                                ctx.message.author.id
                            )
                            )
        self.connection.commit()

    @commands.command()
    async def m_start(self, ctx):
        self.cursor.execute("SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?",
                            (ctx.guild.id, ctx.message.author.id))
        is_mining_data = self.cursor.fetchone()
        if is_mining_data is None:
            pass
        elif is_mining_data[2] == 0:
            pass
        else:
            await ctx.send("You are already mining!")
            return
        self.cursor.execute(
            "DELETE FROM  is_mining WHERE guild_id = ? AND member_id = ?",
            (
                ctx.guild.id,
                ctx.message.author.id
            )
        )
        self.cursor.execute(
            "INSERT INTO is_mining VALUES (?, ?, 1)",
            (
                ctx.guild.id,
                ctx.message.author.id
            )
        )
        self.connection.commit()
        user_data = self.get_user_data(ctx.message.author, ctx.guild)
        server = ctx.guild
        member = ctx.message.author
        discord_message = await ctx.send("System is booting...")
        await asyncio.sleep(5)
        mined_moneys = 0
        while True:
            self.cursor.execute(
                "SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?",
                (
                    server.id,
                    member.id
                )
            )
            is_mining_data = self.cursor.fetchone()
            if is_mining_data is None:
                return
            elif is_mining_data[2] == 0:
                return
            embed = discord.Embed(
                title=f"{ctx.message.author.name}'s cryptofarm!",
                description=f"Farm for mining crypto coins!",
                color=0x00AAFF
            )
            embed.set_thumbnail(
                url=ctx.message.author.avatar_url
            )
            self.cursor.execute(
                "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
                (
                    ctx.guild.id,
                    ctx.message.author.id
                )
            )
            result = self.cursor.fetchall()
            for element in result:
                msg = ""
                mined_moneys_for_one = int(
                    self.moneys_[element[2]]
                ) / (6 * 60 * 24) * random.randint(1, 100) * element[3]
                mined_moneys += mined_moneys_for_one
                msg += f"Cash: {mined_moneys_for_one} crypto coins!\n"
                chances_to_broke = int(
                    self.chances_to_broke[list(self.prises.keys()).index(str(element[2]))]
                )
                un_chances = 100 - chances_to_broke
                amount_of_broken = 0

                for i in range(int(element[3])):
                    random_number = random.randint(0, un_chances)
                    another_random_number = random.randint(0, un_chances)
                    if (random_number == another_random_number):
                        amount_of_broken += 1

                if amount_of_broken != 0:
                    msg += f"{amount_of_broken} of videocards was broken\n"
                    self.delete_videocards(
                        element[2],
                        amount_of_broken,
                        ctx.guild,
                        ctx.message.author
                    )
                embed.add_field(
                    name=f"{element[2].title()} videocards mining information:",
                    value=f"{msg}"
                )
                embed.set_footer(
                    text=f"Налог: {mined_moneys_for_one / 5} 💰\nСчет за электричество: {mined_moneys_for_one / 8} 💰"
                )
            await discord_message.edit(embed=embed)
            self.cursor.execute(
                "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[3] + int(mined_moneys),
                    member.id,
                    server.id
                )
            )
            self.connection.commit()
            await asyncio.sleep(10)

    def delete_videocards(self, videocard, amount, guild, member):
        self.cursor.execute(
            "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
            (
                guild.id,
                member.id,
                videocard
            )
        )
        result = self.cursor.fetchone()
        if result[3] < amount:
            amount = result[3]
        self.cursor.execute(
            "UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND "
            "graphics_cards_name = ?",
            (
                result[3] - amount,
                guild.id,
                member.id,
                videocard
            )
        )
        self.connection.commit()

    def add_videocard(self, videocard, guild, member):
        self.cursor.execute(
            "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
            (
                guild.id,
                member.id,
                videocard
            )
        )
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute(
                "INSERT INTO graphics_cards VALUES (?, ?, ?, ?)",
                (
                    guild.id,
                    member.id,
                    videocard,
                    1
                )
            )
        else:
            self.cursor.execute(
                "UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND "
                "graphics_cards_name = ?",
                (
                    result[3] + 1,
                    guild.id,
                    member.id,
                    videocard
                )
            )
        self.connection.commit()
        return

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
            self.connection.commit()
            data = self.cursor.fetchone()
            return (
                server.id,
                member.id,
                0,
                0
            )
        return data


# setup for cog
def setup(client):
    client.add_cog(MiningCog(client))
