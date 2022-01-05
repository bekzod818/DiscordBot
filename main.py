import discord
from discord.ext import commands
from config import TOKEN, ID, hello_words, goodbye_words

client = commands.Bot(command_prefix=".")
# .start

@client.event
async def on_ready():
    print("Bot connected")


@client.event
async def on_message(message):
    msg = message.content.lower()
    if msg in hello_words:
        await message.channel.send("Assalomu aleykum nima xizmat!")

    if msg in goodbye_words:
        await message.channel.send("Mayli xayr yana keling!")

# @client.command(pass_context=True)
# async def start(ctx, arg=None):
#     author = ctx.message.author
#     await ctx.send(f"Hello {author.mention}, I am a Bot for Discord\nYou are send: {arg}")


# Connect
token = TOKEN

client.run(token)
