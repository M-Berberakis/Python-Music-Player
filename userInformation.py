import sqlite3

databseConnection = sqlite3.connect("userInformation.db")
databaseCursor = databseConnection.cursor()

databaseCursor.execute("""CREATE TABLE userInformation (
        userID INTEGER PRIMARY KEY,
        userLog VARCHAR(255) NOT NULL,
        userPass VARCHAR(255) NOT NULL
        )""")

databseConnection.commit()
