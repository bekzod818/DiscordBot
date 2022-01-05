import os
import discord
from datetime import datetime
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


@client.event
async def on_member_join(member):
    channel = client.get_channel(927646643443073096)
    role = discord.utils.get(member.guild.roles, id = 928377798488358942)
    
    await member.add_roles(role)
    await channel.send(embed = discord.Embed(title = f"Kanalga xush kelibsiz ``{member.name}``", colour = discord.Color.yellow()))


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def user_mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name = "Mute")

    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention} qoidalarga rioya qilmadingiz!")

# Connect
token = os.getenv("TOKEN")

client.run(token)
