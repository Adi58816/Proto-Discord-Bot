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




class Ferma(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prises = {
			"rtx 3090": "32930",
			"6900 xt": "24150",
			"rtx 3080": "27350",
			"6800 xt": "16790",
			"rtx 3070": "16800",
			"rtx 2080 ti": "16440",
			"rtx a6000": "6086",
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
		await ctx.send(file = discord.File(fp = "video_card_ferm.png"))


	@commands.command()
	async def m_buy(self, ctx, *videocard_words):
		videocard = " ".join(videocard_words)
		if not (videocard in list(self.prises.keys())):
			await ctx.send("This videocard doesn NOT exists!")
			print(list(self.prises.keys()))
			print(videocard)
		else:
			user_data = self.get_user_data(ctx.message.author, ctx.guild)
			wallet = user_data[3]
			member = ctx.message.author
			server = ctx.guild
			# getting videocard's prise
			prise = int(self.prises[videocard])
			if (prise > wallet):
				await ctx.send("You don't have this amount of moneys!")
			else:
				self.add_videocard(videocard, server, member)

				self.cursor.execute(
				"UPDATE `economic` SET `wallet_balance` = ? WHERE `member_id` = ? AND `guild_id` = ?",
				((user_data[3] - int(prise)), member.id, server.id)
				)
			self.connection.commit()

	@commands.command()
	async def m_my_farm(self, ctx):
		self.cursor.execute(
			"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
			(ctx.guild.id, ctx.message.author.id)
		)
		result = self.cursor.fetchall()
		# for element in result:
		# 	await ctx.send(f"You have {element[3]} {element[2]} graphics cards!")
		embed = discord.Embed(title = f"{ctx.message.author.name}'s cryptofarm!", description=f"Farm for mining crypto coins!", color=0x00AAFF)
		embed.set_thumbnail(url=ctx.message.author.avatar_url)
		# embed.set_image(url="https://image.freepik.com/free-vector/bank-building-icon_18591-39512.jpg")
		for element in result:
			embed.add_field(name=f"{element[2].title()} videocards:", value=f"Amount: {element[3]}\nManufacturer: {self.videocards_companies[list(self.prises.keys()).index(element[2])]}")
		await ctx.send(embed = embed)

	@commands.command()
	async def m_end_mining(self, ctx):
		self.cursor.execute("DELETE FROM  is_mining WHERE guild_id = ? AND member_id = ?", (ctx.guild.id, ctx.message.author.id))
		self.cursor.execute("INSERT INTO is_mining VALUES (?, ?, 0)", (ctx.guild.id, ctx.message.author.id))
		self.connection.commit()

	@commands.command()
	async def m_start_mining(self, ctx):
		self.cursor.execute("SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?", (ctx.guild.id, ctx.message.author.id))
		is_mining_data = self.cursor.fetchone()
		if is_mining_data is None:
			pass
		elif is_mining_data[2] == 0:
			pass
		else:
			await ctx.send("You are already mining!")
			return
		self.cursor.execute("DELETE FROM  is_mining WHERE guild_id = ? AND member_id = ?", (ctx.guild.id, ctx.message.author.id))
		self.cursor.execute("INSERT INTO is_mining VALUES (?, ?, 1)", (ctx.guild.id, ctx.message.author.id))
		self.connection.commit()
		self.cursor.execute(
			"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
			(ctx.guild.id, ctx.message.author.id)
		)
		result = self.cursor.fetchall()
		user_data = self.get_user_data(ctx.message.author, ctx.guild)
		server = ctx.guild
		member = ctx.message.author
		# for element in result:
		# 	mined_moneys = int(self.prises[element[2]]) / (6 * 60 * 24) * random.randint(1, 100)
		# 	msg += f"{element[2].title()} graphics card mined {mined_moneys} crypto coins for you!\n"
		# discord_message = await ctx.send(msg)
		
		# self.cursor.execute(
		# 	f"UPDATE `economic` SET `wallet_balance` = {user_data[3] + int(mined_moneys)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
		# )
		# self.connection.commit()
		discord_message = await ctx.send("System is booting...")
		await asyncio.sleep(5)
		mined_moneys = 0
		while True:
			self.cursor.execute("SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?", (ctx.guild.id, ctx.message.author.id))
			is_mining_data = self.cursor.fetchone()
			if is_mining_data is None:
				return
			elif is_mining_data[2] == 0:
				return
			embed = discord.Embed(title = f"{ctx.message.author.name}'s cryptofarm!", description=f"Farm for mining crypto coins!", color=0x00AAFF)
			embed.set_thumbnail(url=ctx.message.author.avatar_url)
			
			for element in result:
				msg = ""
				mined_moneys_for_one = int(self.prises[element[2]]) / (6 * 60 * 24) * random.randint(1, 100) * element[3]
				mined_moneys += mined_moneys_for_one
				msg += f"Cash: {mined_moneys_for_one} crypto coins!\n"
				chances_to_broke = int(self.chances_to_broke[list(self.prises.keys()).index(str(element[2]))])
				un_chances = 100 - chances_to_broke
				amount_of_broken = 0
				for i in range(int(element[3])):
					random_number = random.randint(0, un_chances)
					another_random_number = random.randint(0, un_chances)
					if (random_number == another_random_number):
						amount_of_broken += 1
				if amount_of_broken != 0:
					msg += f"{amount_of_broken} of videocards was broken\n"
					self.delete_videocards(element[2], amount_of_broken, ctx.guild, ctx.message.author)
				
				embed.add_field(name=f"{element[2].title()} videocards mining information:", value=f"{msg}")
		
			await discord_message.edit(embed = embed)
			self.cursor.execute(
				f"UPDATE `economic` SET `wallet_balance` = {user_data[3] + int(mined_moneys)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
			)
			self.connection.commit()
			await asyncio.sleep(10)

	def delete_videocards(self, videocard, amount, guild, member):
		self.cursor.execute(
			"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
			(guild.id, member.id, videocard)
		)
		result = self.cursor.fetchone()
		self.cursor.execute(
				"UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
				(result[3] - amount, guild.id, member.id, videocard)
			)
		self.connection.commit()

	def add_videocard(self, videocard, guild, member):
		self.cursor.execute(
			"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
			(guild.id, member.id, videocard)
		)
		result = self.cursor.fetchone()
		if result is None:
			self.cursor.execute(
				"INSERT INTO graphics_cards VALUES (?, ?, ?, ?)",
				(guild.id, member.id, videocard, 1)
			)
		else:
			self.cursor.execute(
				"UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
				(result[3] + 1, guild.id, member.id, videocard)
			)
		self.connection.commit()
		return

	def get_user_data(self, member, server):
		self.cursor.execute(
			f"SELECT * FROM `economic` WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
		)
		data = self.cursor.fetchone()
		if data is None:
			self.cursor.execute(
				f"INSERT INTO `economic` (`guild_id`, `member_id`, `bank_balance`, `wallet_balance`) VALUES ({server.id}, {member.id}, 0, 0)"
			)
			self.connection.commit()
			data = self.cursor.fetchone()
			return (server.id, member.id, 0, 0)
		return data


# setup for cog
def setup(client):
	client.add_cog(Ferma(client))
