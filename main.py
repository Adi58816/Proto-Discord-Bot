import discord
import sys
import os
import config
import sqlite3
from loguru import logger
from discord.ext import commands
import string
import re

logger.add("logs/log.log", format="{level} -> {message} at {time}", level="INFO", rotation="2 MB",
           compression="zip")


def get_prefix(client, message):
    cursor.execute("SELECT * FROM prefixes WHERE guild_id = ?", (message.guild.id,))
    result = cursor.fetchone()
    if result is None:
        return "/"
    else:
        return result[1]


# discord bot object 
bot = commands.Bot(command_prefix=get_prefix)
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
bot.logger = logger


@bot.event
async def on_ready():
    logger.info("Discord.bot.guilds are ready!")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("python bot.py"))


@bot.event
async def on_message(msg):
    guild_id = msg.guild.id
    prefix = get_prefix(bot, msg)
    cursor.execute(
        "SELECT * FROM log_channel WHERE guild_id = ?",
        (
            guild_id,
        )
    )
    result = cursor.fetchone()
    amount_of_big_letters = 0
    REGEX_EN = re.compile(r"[A-Z]")
    REGEX_RU = re.compile(r"[А-Я]")
    amount_of_big_letters += len(REGEX_EN.findall(msg.content))
    amount_of_big_letters += len(REGEX_RU.findall(msg.content))
    if amount_of_big_letters > 5 and msg.author != bot.user:
        if result is not None:
            logger.info(f"Caps detected from user {msg.author.id} on server {msg.guild.id}, message: {msg.content}!")
            channel = discord.utils.get(msg.guild.channels, id=int(result[1]))
            embed = discord.Embed(title=f":no_entry: CAPS", description=f"Member used lots of BIG LETTERS:")
            embed.add_field(name=f"Message: {msg.content}", value=f"Amount of BIG LETTERS: {amount_of_big_letters}",
                            inline=False)
            embed.add_field(name=f"Channel: {msg.channel.name}", value=f"Message id: {msg.id}", inline=False)
            embed.set_thumbnail(
                url=msg.author.avatar_url
            )
            try:
                logger.info(
                    f"Message was successfully sent to log channel!")
                await channel.send(embed=embed)
            except:
                logger.warning(f"Error of NOT existing log channel on server: {msg.guild.id}")
                await msg.channel.send(
                    "Sorry, but this log channel does not exists or was deleted. If you are adminstrator of this "
                    "discord server just write `/logs_off`")

    if msg.content.startswith(prefix):
        if result is not None:
            channel = discord.utils.get(msg.guild.channels, id=int(result[1]))
            embed = discord.Embed(title=f"Channel: {msg.channel.name}",
                                  description=f"member just tried to execute command:")
            embed.add_field(name=f"user {msg.author.name} executed command:", value=f"`{msg.content}`", inline=False)
            embed.set_thumbnail(
                url=msg.author.avatar_url
            )
            try:
                logger.info(
                    f"""executing command \"{msg.content}\", by {msg.author.id} on {msg.guild.id}""")
                await channel.send(embed=embed)
            except:
                logger.warning(f"error of not existing log channel on server: {msg.guild.id}")
                await msg.channel.send(
                    "sorry, but this log channel does not exists or was deleted. if you are adminstrator of this "
                    "discord server just write `/logs_off`")
        await bot.process_commands(msg)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"""`{error}`""")


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        logger.info(f"importing cog cogs.{file[:-3]}...")


# main function
@logger.catch()
def main():
    logger.info(f"Bot was run successfully!")
    try:
        while True:
            bot.run(config.TOKEN)
    except RuntimeError:
        sys.exit(0)
    logger.warning("Bot was stopped!")


# if package is main running main function
if __name__ == "__main__":
    main()