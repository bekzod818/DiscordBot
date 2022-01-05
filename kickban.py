import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

PREFIX = "."
# .help
client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot connected")


# Delete
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit=amount)


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


# Command help
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)

    emb = discord.Embed(title="Barcha buyruqlar")

    emb.add_field(name="{}clear".format(PREFIX), value="Chatni tozalash")
    emb.add_field(name="{}kick".format(PREFIX), value="Foydalanuvchini o'chirish")
    emb.add_field(name="{}ban".format(PREFIX), value="Ban qilish")
    emb.add_field(name="{}unban".format(PREFIX), value="UnBan qilish")

    await ctx.send(embed = emb)



# Connect
token = os.getenv("TOKEN")

client.run(token)
