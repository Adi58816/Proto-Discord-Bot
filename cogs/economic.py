import sqlite3
import asyncio
import os
import sys
from loguru import logger
import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import cog_ext


class EconomyCog(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.conn = sqlite3.connect("database.db")
		self.cursor = self.conn.cursor()

	@commands.command()
	async def bal(self, ctx):
		data = self.get_user_data(
			ctx.message.author, 
			ctx.guild
		)
		embed = discord.Embed(
			title = "Users' balance", 
			description = f"User: {ctx.message.author.mention}", 
			color = 0x00AAFF
		)
		embed.set_thumbnail(
			url = ctx.message.author.avatar_url
		)
		embed.add_field(
			name = "Server", 
			value = ctx.guild.name
		)
		embed.add_field(
			name = "Wallet", 
			value = f"{data[3]} 💸"
		)
		embed.add_field(
			name = "Bank", 
			value = f"{data[2]} 💰"
		)
		await ctx.send(
			embed = embed
		)


	@commands.command()
	async def gbal(self, ctx, member: discord.Member):
		data = self.get_user_data(member, ctx.guild)
		embed = discord.Embed(
			title = "Users' balance", 
			description = f"User: {member.mention}", 
			color = 0x00AAFF)
		embed.set_thumbnail(
			url = member.avatar_url
		)
		embed.add_field(
			name = "Server", 
			value = ctx.guild.name
		)
		embed.add_field(
			name = "Wallet", 
			value = f"{data[3]} 💸"
		)
		embed.add_field(
			name = "Bank", value = f"{data[2]} 💰"
		)
		await ctx.send(
			embed = embed
		)

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(
			"pong"
		)

	@commands.has_permissions(
		administrator = True
	)
	@commands.command()
	async def set_wallet(self, ctx, member: discord.Member, balance: int):
		server = ctx.guild
		self.cursor.execute(
			"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
			(
				balance,
				member.id, 
				server.id
			)
		)
		self.conn.commit()

	@commands.has_permissions(
		administrator = True
	)
	@commands.command()
	async def add_bal(self, ctx, member: discord.Member, balance: int):
		user_data = self.get_user_data(
			member, 
			ctx.guild
		)
		server = ctx.guild
		self.cursor.execute(
			"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
			(
				int(user_data[3]) + int(balance), 
				member.id,
				server.id
			)
		)
		self.conn.commit()

	@commands.command()
	async def send_gift(self, ctx, member: discord.Member, cash: int):
		user_data = self.get_user_data(
			ctx.message.author, 
			ctx.guild
		)
		getter_balance = int(
			self.get_user_data(
				member, 
				ctx.guild
			)[3]
		)
		users_balance = int(
			user_data[3]
		)
		if int(cash) > users_balance:
			await ctx.send(
				f"{ctx.message.author.mention} You don't have so much moneys!"
			)
		else:
			self.cursor.execute(
				"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					users_balance - int(cash),
					ctx.message.author.id,
					ctx.guild.id
				)
			)
			self.cursor.execute(
				"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					getter_balance + int(cash),
					member.id,
					ctx.guild.id
				)
			)
			self.conn.commit()

	@commands.has_permissions(administrator = True)
	@commands.command()
	async def del_bal(self, ctx, member: discord.Member, balance: int):
		user_data = self.get_user_data(
			member, 
			ctx.guild
		)
		server = ctx.guild
		if user_data[3] < int(balance):
			await ctx.send(
				f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}"
			)
		else:
			self.cursor.execute(
				"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					user_data[3] - int(balance),
					member.id,
					server.id
				)
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
				"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					user_data[3] - int(balance),
					member.id,
					server.id
				)
			)
			self.cursor.execute(
				"UPDATE economic SET bank_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					user_data[2] + int(balance),
					member.id,
					server.id
				)
			)
			self.conn.commit()
			
	@commands.command()
	async def from_bank(self, ctx, balance: int):
		member = ctx.message.author 
		user_data = self.get_user_data(member, ctx.guild)
		server = ctx.guild
		if user_data[2] < int(balance):
			await ctx.send(
				f"{ctx.message.author.mention} You can't delete this amount of moneys from user {member.mention}"
			)
			return
		else:
			self.cursor.execute(
				"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					user_data[3] + int(balance),
					member.id,
					server.id
				)
			)
			self.cursor.execute(
				"UPDATE economic SET bank_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					user_data[2] - int(balance),
					member.id,
					server.id
				)
			)
			self.conn.commit()


	@commands.has_permissions(administrator = True)
	@commands.command()
	async def add_shop_item(self, ctx, role: discord.Role, prise: int):
		self.cursor.execute(
			"INSERT INTO economic_shop_item VALUES(?, ?, ?)",
			(
				ctx.guild.id,
				role.id,
				prise
			)
		)
		self.conn.commit()

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
			self.conn.commit()
			data = self.cursor.fetchone()
			return (server.id, member.id, 0, 0)
		return data

	@commands.command()
	async def shop(self, ctx):
		self.cursor.execute(
			"SELECT * FROM economic_shop_item WHERE guild_id = ?",
			(
				ctx.guild.id,
			)
		)
		data = self.cursor.fetchall()
		msg = ""
		for item in data:
			msg += f"{ctx.guild.get_role(item[1]).mention} costs {item[2]}\n"

		await ctx.send(msg)

	@commands.command()
	async def buy(self, ctx, role: discord.Role):
		self.cursor.execute(
			"SELECT * FROM economic_shop_item WHERE guild_id = ?",
			(
				ctx.guild.id,
			)
		)
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
					"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
					(
						user_data[3] - int(balance),
						ctx.message.author.id,
						server.id
					)
				)
				self.conn.commit()
				await ctx.message.author.add_roles(role)
				await ctx.send(f"You got role {role.mention}. Thank you for paying!")

# setup function
def setup(client):
	client.add_cog(EconomyCog(client))
