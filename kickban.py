import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix=".")
# .start

@client.event
async def on_ready():
    print("Bot connected")

# Kick User
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit=1)

    await member.kick(reason=reason)
    await ctx.send(f'Kick user {member.mention}')

# Ban User
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)
    await ctx.send(f"Ban user {member.mention}")

# UnBan User
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned user {user.mention}")

        return


# Connect
token = os.getenv("TOKEN")

client.run(token)
