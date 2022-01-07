import sqlite3
import os
import discord
import giphy_client
from giphy_client.rest import ApiException
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

PREFIX = "/"
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command('help')

conn = sqlite3.connect("discord.db")
cursor = conn.cursor()

@client.event
async def on_ready():
    print("Bot connected")
    for guild in client.guilds:#т.к. бот для одного сервера, то и цикл выводит один сервер
        print(guild.id)#вывод id сервера
        serv=guild#без понятия зачем это
        for member in guild.members:#цикл, обрабатывающий список участников
            if member != client.user:
                cursor.execute(f"SELECT id FROM users where id={member.id}")#проверка, существует ли участник в БД
                if cursor.fetchone() == None:#Если не существует
                    cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', 1, 1)")#вводит все данные об участнике в БД
                else:#если существует
                    pass
            conn.commit()#применение изменений в БД

# Join channel
@client.event
async def on_member_join(member):
    # print(dir(member.guild))
    cursor.execute(f"SELECT id FROM users where id={member.id}")#все также, существует ли участник в БД
    if cursor.fetchone()==None:#Если не существует
        cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}',1,1)")#вводит все данные об участнике в БД
        channel = member.guild.system_channel
        await channel.send(embed = discord.Embed(title = f"``{member.name}`` connected to the channel", colour = discord.Color.green()))
    else:#Если существует
        pass
    conn.commit()#применение изменений в БД


# Left channel
@client.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.send(embed = discord.Embed(title = f"``{member.name}`` left channel!", colour = discord.Color.red()))
    cursor.execute(f"DELETE FROM users WHERE id={member.id}")#вводит все данные об участнике в БД
    conn.commit()#применение изменений в БД

# Message
@client.event
async def on_message(message):
    for row in cursor.execute(f"SELECT MSG, LVL FROM users where id={message.author.id}"):
        cnt = row[0] + 1
        cursor.execute(f'UPDATE users SET MSG={cnt} where id={message.author.id}')

        if row[0] % 20 == 0:
            lvl = row[1] + 1
            cursor.execute(f'UPDATE users SET LVL={lvl} where id={message.author.id}')
            emb = discord.Embed(
                title=f":chart_with_upwards_trend: Congratulations {message.author.name}!",
                description=f"Your level is up to {row[1]}"
            )
            await message.channel.send(embed=emb)
            # await message.channel.send(f'{row[1]}-LEVEL {message.author.name}!')


    await client.process_commands(message)#Далее это будет необходимо для ctx команд
    conn.commit()#применение изменений в БД


# listgames
@client.command()
async def listgames(ctx):
    lst = cursor.execute(f"SELECT title, desc, url, rating FROM games").fetchall()
    for row in lst:
        emb = discord.Embed(title=f"{row[0]}", description = f"{row[1]}", colour = discord.Color.blue())
        emb.set_image(url = f"{row[2]}")
        emb.add_field(name = "Rating", value=row[3])
        await ctx.send(embed = emb)


# Command help
@client.command()
async def help(ctx):
    await ctx.send(f"Hello {ctx.author.name}")


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


# Gif command
@client.command()
async def gif(ctx, *, q = "Smile"):
    api_key = os.getenv("API_KEY")
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating="g")
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title = q.title(), colour = discord.Color.green())
        emb.set_image(url = f"https://media.giphy.com/media/{giff.id}/giphy.gif")
        await ctx.channel.send(embed=emb)

    except ApiException as e:
        print("Exception when calling DefaultApi -> gifs_search_get: %s\n" % e)


# Connect
token = os.getenv("TOKEN")

client.run(token)
