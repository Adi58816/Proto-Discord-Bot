import discord
import os
import asyncio
import youtube_dl
from discord.ext import commands


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx, url):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = ctx.message.author.voice.channel
        try:
            await voiceChannel.connect()
        except:
            pass
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        await ctx.send("Downloading...")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        await ctx.send("Running...")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command()
    async def leave(self, ctx):
        # voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice_client = ctx.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()


# setup for cog
def setup(client):
    client.add_cog(Music(client))
