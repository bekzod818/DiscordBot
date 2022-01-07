import sqlite3
import requests
import random

#Connecting to sqlite
conn = sqlite3.connect('discord.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS USERS")
cursor.execute("DROP TABLE IF EXISTS GAMES")

#Creating table as per requirement
sql ='''CREATE TABLE USERS(
   ID INT,
   NAME CHAR(50) NOT NULL,
   MSG INT,
   LVL INT
)'''

games ='''CREATE TABLE GAMES(
   TITLE CHAR(50) NOT NULL,
   DESC CHAR(150) NOT NULL,
   URL CHAR(150) NOT NULL,
   RATING CHAR(10) NOT NULL
)'''

cursor.execute(sql)
cursor.execute(games)
print("Tables created successfully........")

# requests json
res = requests.get(url = "https://www.freetogame.com/api/games").json()

add = ''' INSERT INTO games(title,desc,url,rating)
              VALUES(?,?,?,?) '''
for i in range(5):
    cursor.execute(add, (f'{res[i]["title"]}', f'{res[i]["short_description"]}', f'{res[i]["thumbnail"]}', f'{random.randint(30, 50) / 10}'))

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()
