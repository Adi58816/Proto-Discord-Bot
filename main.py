import discord
import sys
import os
import config
import sqlite3
from loguru import logger
from discord.ext import commands
from discord_slash import SlashCommand


logger.add("logs/log_{time}.json", format="{level}: {message}", level="INFO", serialize=True, rotation="200 MB", compression = "zip")


def get_prefix(client, message):
    cursor.execute("SELECT * FROM prefixes WHERE guild_id=?", (message.guild.id, ))
    result = cursor.fetchone()
    if result is None:
        return "/"
    else:
        return result[1]


# discord bot object 
bot = commands.Bot(command_prefix = get_prefix)
slash = SlashCommand(bot, sync_commands = True)
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


@bot.event
async def on_ready():
    logger.info("Discord.bot.guilds are ready!")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("python bot.py"))

@bot.event
async def on_message(msg):
    guild_id = msg.guild.id
    prefix = get_prefix(bot, msg)
    if msg.content.startswith(prefix):
        cursor.execute(
            "SELECT * FROM log_channel WHERE guild_id = ?", 
            (
                guild_id, 
            )
        )
        result = cursor.fetchone()
        if result is not None:
            channel = discord.utils.get(msg.guild.channels, id=int(result[1]))
            embed = discord.Embed(title="Logs", description=f"Server: {msg.guild.name}")
            embed.add_field(name=f"User {msg.author.name} executed command:", value=f"`{msg.content}`", inline=False)  
            embed.set_thumbnail(
                url = msg.author.avatar_url
            )
        await channel.send(embed=embed)
        await bot.process_commands(msg)

@bot.event 
async def on_command_error(ctx, error):
    await ctx.send(f"""||`{error}`||""")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        logger.info(f"COG {file} was loaded")


# @bot.event
# async def on_member_join(ctx, member):
#     channel = member.server.default_channel
#     await bot.send(channel, f"Welcome {member.mention}!")
    
# main function
def main():
    logger.info(f"BOT WAS RUNNED SUCCESSFULY!")
    bot.run(os.getenv("BOT_TOKEN"))
    logger.warning("BOT WAS STOPPED!")


# if package is main running main function
if __name__ == "__main__":
    main()
