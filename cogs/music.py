import discord
import os
import asyncio
import youtube_dl
from discord.ext import commands
from youtube_search import YoutubeSearch


class Music(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def play(self, ctx, *url_words):
		url = " ".join(url_words)
		try:
			voice = discord.utils.get(
			self.client.voice_clients,
				guild=ctx.guild
			)
			voice.stop()
		except:
			pass
		FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		ydl_opts = {'format': 'bestaudio'}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			try:
				info = ydl.extract_info(url, download=False)
			except:
				await ctx.send("Searching video...")
				to_search = url
				results = YoutubeSearch(to_search, max_results=1).to_dict()
				NEW_URL = ("https://youtube.com" + results[0]["url_suffix"])
				info = ydl.extract_info(NEW_URL, download = False)
				await ctx.send(f"Found: {NEW_URL}")
			URL = info['formats'][0]['url']
		await ctx.send("Downloading...")
		await ctx.send("Running audio...")
		voiceChannel = ctx.message.author.voice.channel
		try:
			await voiceChannel.connect()
		except:
			pass
		voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
		voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

	@commands.command()
	async def leave(self, ctx):
		voice_client = ctx.guild.voice_client
		if voice_client:
			await voice_client.disconnect()
		else:
			await ctx.send(
				"The bot is not connected to a voice channel."
			)

	@commands.command()
	async def pause(self, ctx):
		voice = discord.utils.get(
			self.client.voice_clients,
			guild=ctx.guild
		)
		if voice.is_playing():
			voice.pause()
		else:
			await ctx.send(
				"Currently no audio is playing."
			)

	@commands.command()
	async def resume(self, ctx):
		voice = discord.utils.get(
			self.client.voice_clients,
			guild=ctx.guild
		)
		if voice.is_paused():
			voice.resume()
		else:
			await ctx.send(
				"The audio is not paused."
			)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def stop(self, ctx):
		voice = discord.utils.get(
			self.client.voice_clients,
			guild=ctx.guild
		)
		voice.stop()


# setup for cog
def setup(client):
	client.add_cog(Music(client))
