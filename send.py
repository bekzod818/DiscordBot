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


@client.command()
async def send_a(ctx):
    await ctx.channel.purge(limit = 1)
    await ctx.author.send("Men Discord Botman 🤖")

@client.command()
async def send_m(ctx, member: discord.Member):
    await ctx.channel.purge(limit = 1)
    await member.send(f"{member.name}, salom bu men {ctx.author.name}")


# Connect
token = os.getenv("TOKEN")

client.run(token)
