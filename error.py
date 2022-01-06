import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from config import bad_words

load_dotenv()

client = commands.Bot(command_prefix=".")
# .start

@client.event
async def on_ready():
    print("Bot connected")
    # status bot
    await client.change_presence(status = discord.Status.online, activity = discord.Game('help'))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("Noto'g'ri buyruq berildi")


# Filter
@client.event
async def on_message(message):
    await client.process_commands(message)

    msg = message.content.lower()

    if msg in bad_words:
        await message.delete()
        await message.author.send(f"{message.author.name} yomon so'zlar ishlatmang!")



# Delete
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


# Error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.name}, nechta xabar o'chirishni sonini ham bering!")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.name} sizda buni qilishga ruxsat yo'q!")

#join
@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f"Bot {channel} kanaliga qo'shildi")

# leave
@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send(f"Bot {channel} kanalini tark etdi!")



# Connect
token = os.getenv("TOKEN")

client.run(token)
