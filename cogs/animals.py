import discord
import json
import requests
from discord.ext import commands

class Animals(commands.Cog):

	def __init__(self, client):
		self.client = client 

	@commands.command()
	async def fox(self, ctx):
	    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
	    json_data = json.loads(response.text) # Извлекаем JSON

	    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
	    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	    await ctx.send(embed = embed) # Отправляем Embed

	@commands.command()
	async def dog(self, ctx):
	    response = requests.get('https://some-random-api.ml/img/dog') # Get-запрос
	    json_data = json.loads(response.text) # Извлекаем JSON

	    embed = discord.Embed(color = 0xff9900, title = 'Random Dog') # Создание Embed'a
	    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	    await ctx.send(embed = embed) # Отправляем Embed

	@commands.command()
	async def cat(self, ctx):
	    response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
	    json_data = json.loads(response.text) # Извлекаем JSON

	    embed = discord.Embed(color = 0xff9900, title = 'Random Cat') # Создание Embed'a
	    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
	    await ctx.send(embed = embed) # Отправляем Embed

def setup(client):
	client.add_cog(Animals(client))