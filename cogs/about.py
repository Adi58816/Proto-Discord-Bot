# importing modules
import discord
import requests
import io
import sqlite3
import json
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from datetime import datetime


class AboutCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect(
            "database.db"
        )
        self.cursor = self.conn.cursor()

    @commands.command()
    async def myroles(self, ctx):
        member = ctx.message.author
        msg = "|\t"
        for role in member.roles:
            if role.name != "@everyone":
                msg += role.name + "\t|\t"

        await ctx.send(
            msg
        )

    @commands.command()
    async def name(self, ctx):
        await ctx.send(
            "Your name is <@{.fauthor.id}>".format(
                ctx
            )
        )

    @commands.command()
    async def card(self, ctx, member: discord.Member):
        img = Image.open(
            'icon_template.png'
        )
        url = str(member.avatar_url)[:-10]

        try:
            response = requests.get(
                url, 
                stream = True
            )
            response = Image.open(
                io.BytesIO(
                    response.content
                )
            )
            response = response.convert(
                'RGBA'
            )
            response = response.resize(
                (
                    100, 
                    100
                ), 
                Image.ANTIALIAS
            )
        except:
            pass

        try:
            img.paste(
                response, 
                (15, 15, 115, 115)
            )
        except:
            pass

        idraw = ImageDraw.Draw(
            img
        )
        name = member.name
        tag = member.discriminator

        headline = ImageFont.truetype(
            "./Play-Regular.ttf", 
            size = 17
        )
        undertext = ImageFont.truetype(
            "./Play-Regular.ttf", 
            size = 12
        )
        undertext2 = ImageFont.truetype(
            "./Play-Regular.ttf", 
            size = 10
        )

        idraw.text(
            (
                120, 
                15
            ), 
            f'{name}#{tag}', 
            font = headline)
        idraw.text(
            (
                120, 
                35
            ), 
            f'ID: {ctx.author.id}', 
            font = undertext)

        time_stamp = member.created_at.timestamp()
        time_formated = datetime.fromtimestamp(
            time_stamp
        ).strftime("%A, %B %d, %Y %I:%M:%S")
        idraw.text(
            (120, 55), 
            f'Date of registration: {time_formated}', 
            font = undertext2
        )

        img.save(
            'card.png'
        )
        await ctx.send(
            file=discord.File(
                fp='card.png'
            )
        )

    @commands.command()
    async def whoami(self, ctx):
        if ctx.message.author.guild_permissions.administrator:
            await ctx.send(
                "<@{.author.id}> are administrator".format(
                    ctx
                )
            )
        else:
            await ctx.send(
                "<@{.author.id}> You are just man :|".format(
                    ctx
                )
            )

    @commands.command()
    async def avatar(self, ctx):
        author = ctx.author
        await ctx.send(
            author.avatar_url
        )

    @commands.command()
    async def guild_name(self, ctx):
        await ctx.send(
            ctx.guild.name
        )

# setup for cog
def setup(client):
    client.add_cog(AboutCog(client))
    
