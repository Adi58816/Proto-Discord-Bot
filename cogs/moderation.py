import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member: discord.Member):
        await member.send("You was banned :(")
        await member.ban(reason="Ban!")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")


        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.Member):
        await member.send("You was kicked :(")
        await member.kick()

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send("Chat was cleaned by <@{.author.id}>".format(ctx))
        
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def clear_all(self, ctx):
        await ctx.channel.purge()
        await ctx.send("Chat was cleaned by <@{.author.id}>".format(ctx))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def send_to(self, ctx, member: discord.Member, *args):
        await member.send(f"<{ctx.author.name}> sended you this message: {' '.join(args)}")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        try:
            await member.add_roles(role)
            await ctx.send(f"<@{ctx.author.id}> has gived role {role} to <@{member.id}>")
        except:
            await ctx.send(f"<@{ctx.author.id}> you are missing permissions")    \

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        try:
            await member.remove_roles(role)
            await ctx.send(f"<@{ctx.author.id}> has removed role {role.mention} from <@{member.id}>")
        except:
            await ctx.send(f"<@{ctx.author.id}> you are missing permissions")

# setup for cog
def setup(client):
    client.add_cog(Moderation(client))
