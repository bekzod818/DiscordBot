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

# Delete
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit=amount)

# Clear command
@client.command(pass_context=True)
async def hello(ctx, amount=1):
    await ctx.channel.purge(limit=amount)

    author = ctx.message.author
    await ctx.send(f"Hello {author.mention}")


# Connect
token = os.getenv("TOKEN")

client.run(token)
