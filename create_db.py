import mysql.connector

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user= "root", 
    password = "password",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
