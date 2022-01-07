import sqlite3
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

PREFIX = "."
client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command('help')

conn = sqlite3.connect("discord.db") # или :memory:
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
        await channel.send(embed = discord.Embed(title = f"Welcome ``{member.name}``", colour = discord.Color.green()))
    else:#Если существует
        pass
    conn.commit()#применение изменений в БД


# Left channel
@client.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.send(embed = discord.Embed(title = f"``{member.name}`` left the group!", colour = discord.Color.red()))
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
            await message.channel.send(f'{row[1]} - уровень {message.author.name}!')


    await client.process_commands(message)#Далее это будет необходимо для ctx команд
    conn.commit()#применение изменений в БД

# Command help
@client.command(pass_context=True)
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

# Connect
token = os.getenv("TOKEN")

client.run(token)
