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


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def embed(ctx):
    emb = discord.Embed(title="Embed title", description = "Embed description", colour = discord.Color.green(), url="https://discordpy.readthedocs.io/en/stable/api.html?highlight=embed#embed")

    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_thumbnail(url = "https://www.online-tech-tips.com/wp-content/uploads/2021/02/1-Discord-Canary-Featured.png")
    emb.set_image(url = "https://cdn.mos.cms.futurecdn.net/my8AUCgUhKERqBBwdPQuXG-1024-80.jpg.webp")
    emb.add_field(name = "Now", value=datetime.now())

    await ctx.send(embed = emb)


# Ban User
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    emb = discord.Embed(title = "Ban User", colour = discord.Color.red())
    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)

    emb.set_author(name = member.name, icon_url = member.avatar_url)
    emb.add_field(name = "Banned user", value = member.mention)
    emb.set_footer(text = f"{ctx.author.name} admin tomonidan ban qilindi", icon_url = ctx.author.avatar_url)

    await ctx.send(embed = emb)


# Connect
token = os.getenv("TOKEN")

client.run(token)
