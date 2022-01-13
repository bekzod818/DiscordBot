import os
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix=os.getenv("PREFIX"))
client.remove_command('help')

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

@client.event
async def on_ready():
    print("Bot connected")
    # cursor.execute("""CREATE TABLE users (
    #     name TEXT,
    #     id INT,
    #     cash BIGINT,
    #     rep INT,
    #     lvl INT
    # )""")
    # connection.commit()

    for guild in client.guilds:
        print(guild.id)
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
            else:
                pass
            connection.commit()

@client.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
    else:
        pass
    connection.commit()

client.run(os.getenv("TOKEN"))
