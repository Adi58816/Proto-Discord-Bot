import discord
import os
import config
from loguru import logger
from discord.ext import commands
from discord_slash import SlashCommand


bot = commands.Bot(command_prefix = "/")
# slash = SlashCommand(bot,  SlashCommand(client, sync_commands=True = True)
slash = SlashCommand(bot, override_type =True)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("python bot.py"))


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        logger.info(f"COG {file} was loaded")


def main():
    bot.run(config.TOKEN)
    logger.info(f"BOT WAS RUNNED SUCCESSFULY!")


if __name__ == "__main__":
    main()
