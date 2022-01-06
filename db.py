import sqlite3

#Connecting to sqlite
conn = sqlite3.connect('discord.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS USERS")

#Creating table as per requirement
sql ='''CREATE TABLE USERS(
   ID INT,
   NAME CHAR(50) NOT NULL,
   MSG INT,
   LVL INT
)'''
cursor.execute(sql)
print("Table created successfully........")

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()
