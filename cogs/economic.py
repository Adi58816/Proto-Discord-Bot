# importing sqlite db
import sqlite3

# importing asyncio
import asyncio

# importing os
import os

# python
import sys

# importing module for logging
from loguru import logger

# importing discord
import discord
from discord.ext import commands
from discord.utils import get

# importing slash commands
from discord_slash import cog_ext, SlashContext
from discord_slash import SlashCommand


"""
Just cog for bot economic
"""


class EconomyCog(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.conn = sqlite3.connect("database.db")
		self.cursor = self.conn.cursor()

	@commands.command()
	async def balance(self, ctx):
		data = self.get_user_data(ctx.message.author, ctx.guild)
# 		await ctx.send(f"""{ctx.guild.name} discord server's economic:
# User: {ctx.message.author.name}
# Wallet: {data[3]} 💸
# Bank: {data[2]} 💰""")
		embed = discord.Embed(title = "Users' balance", description=f"User: {ctx.message.author.mention}", color=0x00AAFF)
		embed.set_thumbnail(url=ctx.message.author.avatar_url)
		# embed.set_image(url="https://image.freepik.com/free-vector/bank-building-icon_18591-39512.jpg")
		embed.add_field(name="Server", value=ctx.guild.name)
		embed.add_field(name="Wallet", value=f"{data[3]} 💸")
		embed.add_field(name="Bank", value=f"{data[2]} 💰")
		await ctx.send(embed = embed)


	@commands.command()
	async def get_balance(self, ctx, member: discord.Member):
		data = self.get_user_data(member, ctx.guild)
# 		await ctx.send(f"""{ctx.guild.name} discord server's economic:
# User: {member.name}
# Wallet: {data[3]} 💸
# Bank: {data[2]} 💰""")
		embed = discord.Embed(title = "Users' balance", description=f"User: {member.mention}", color=0x00AAFF)
		embed.set_thumbnail(url=member.avatar_url)
		# embed.set_image(url="https://image.freepik.com/free-vector/bank-building-icon_18591-39512.jpg")
		embed.add_field(name="Server", value=ctx.guild.name)
		embed.add_field(name="Wallet", value=f"{data[3]} 💸")
		embed.add_field(name="Bank", value=f"{data[2]} 💰")
		await ctx.send(embed = embed)

	@commands.command()
	async def ping(self, ctx):
		await ctx.send("pong")

	@commands.has_permissions(administrator = True)
	@commands.command()
	async def set_wallet(self, ctx, balance: int):
		member = ctx.message.author
		server = ctx.guild
		self.cursor.execute(
			f"UPDATE `economic` SET `wallet_balance` = {balance} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
		)
		self.conn.commit()


	# @commands.has_permissions(administrator = True)
	# @commands.command()
	# async def set_bank(self, ctx, balance: int):
	# 	member = ctx.message.author
	# 	server = ctx.guild
	# 	self.cursor.execute(
	# 		f"UPDATE `economic` SET `bank_balance` = {balance} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
	# 	)
	# 	self.conn.commit()

	@commands.has_permissions(administrator = True)
	@commands.command()
	async def add_balance(self, ctx, member: discord.Member, balance):
		user_data = self.get_user_data(member, ctx.guild)
		server = ctx.guild
		self.cursor.execute(
			f"UPDATE `economic` SET `wallet_balance` = {user_data[3] + int(balance)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
		)
		self.conn.commit()

	@commands.command()
	async def send_gift(self, ctx, member: discord.Member, cash):
		user_data = self.get_user_data(ctx.message.author, ctx.guild)
		getter_balance = int(self.get_user_data(member, ctx.guild)[3])
		users_balance = int(user_data[3])
		if int(cash) > users_balance:
			await ctx.send(f"{ctx.message.author.mention} You don't have so much moneys!")
		else:
			self.cursor.execute(
				f"UPDATE `economic` SET `wallet_balance` = {users_balance - int(cash)} WHERE `member_id` = {ctx.message.author.id} AND `guild_id` = {ctx.guild.id}"
			)
			self.cursor.execute(
				f"UPDATE `economic` SET `wallet_balance` = {getter_balance + int(cash)} WHERE `member_id` = {member.id} AND `guild_id` = {ctx.guild.id}"
			)
			self.conn.commit()

	@commands.has_permissions(administrator = True)
	@commands.command()
	async def del_balance(self, ctx, member: discord.Member, balance):
		user_data = self.get_user_data(member, ctx.guild)
		server = ctx.guild
		if user_data[3] < int(balance):
			await ctx.send(
				f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}")
		else:
			self.cursor.execute(
				f"UPDATE `economic` SET `wallet_balance` = {user_data[3] - int(balance)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
			)
			self.conn.commit()

	@commands.command()
	async def to_bank(self, ctx, balance: int):
		member = ctx.message.author 
		user_data = self.get_user_data(member, ctx.guild)
		server = ctx.guild
		if user_data[3] < int(balance):
			await ctx.send(
				f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}")
			return
		else:
			self.cursor.execute(
				f"UPDATE `economic` SET `wallet_balance` = {user_data[3] - int(balance)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
			)
			self.cursor.execute(
				f"UPDATE `economic` SET `bank_balance` = {user_data[2] + int(balance)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
			)
			self.conn.commit()
			
	@commands.command()
	async def from_bank(self, ctx, balance: int):
		member = ctx.message.author 
		user_data = self.get_user_data(member, ctx.guild)
		server = ctx.guild
		if user_data[2] < int(balance):
			await ctx.send(
				f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}")
			return
		else:
			self.cursor.execute(
				f"UPDATE `economic` SET `wallet_balance` = {user_data[3] + int(balance)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
			)
			self.cursor.execute(
				f"UPDATE `economic` SET `bank_balance` = {user_data[2] - int(balance)} WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
			)
			self.conn.commit()


	@commands.has_permissions(administrator = True)
	@commands.command()
	async def add_shop_item(self, ctx, role: discord.Role, prise: int):
		self.cursor.execute(
			f"INSERT INTO `economic_shop_item` (`guild_id`, `role_id`, `prise`) VALUES({ctx.guild.id}, {role.id}, {prise})"
		)
		self.conn.commit()

	def get_user_data(self, member, server):
		self.cursor.execute(
			f"SELECT * FROM `economic` WHERE `member_id` = {member.id} AND `guild_id` = {server.id}"
		)
		data = self.cursor.fetchone()
		if data is None:
			self.cursor.execute(
				f"INSERT INTO `economic` (`guild_id`, `member_id`, `bank_balance`, `wallet_balance`) VALUES ({server.id}, {member.id}, 0, 0)"
			)
			self.conn.commit()
			data = self.cursor.fetchone()
			return (server.id, member.id, 0, 0)
		return data

	@commands.command()
	async def shop(self, ctx):
		self.cursor.execute(f"SELECT * FROM `economic_shop_item` WHERE `guild_id` = {ctx.guild.id}")
		data = self.cursor.fetchall()
		msg = ""
		for item in data:
			msg += f"{ctx.guild.get_role(item[1]).mention} costs {item[2]}\n"

		await ctx.send(msg)

	@commands.command()
	async def buy(self, ctx, role: discord.Role):
		self.cursor.execute(f"SELECT * FROM `economic_shop_item` WHERE `guild_id` = {ctx.guild.id}")
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
					f"UPDATE `economic` SET `wallet_balance` = {user_data[3] - int(balance)} WHERE `member_id` = {ctx.message.author.id} AND `guild_id` = {server.id}"
				)
				self.conn.commit()
				await ctx.message.author.add_roles(role)
				await ctx.send(f"You got role {role.mention}. Thank you for paying!")

def setup(client):
	client.add_cog(EconomyCog(client))
