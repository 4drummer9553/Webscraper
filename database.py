import sqlite3

connection = sqlite3.connect('soccer.db')

cur = connection.cursor()

# Creates table if it exists
cur.execute("""CREATE TABLE IF NOT EXISTS soccer(
                player_name TEXT PRIMARY KEY,
                medals INTEGER,
                country TEXT,
                position TEXT,
                team TEXT,
                first_season TEXT,
                last_season TEXT
                )""")

# Removes a player
def remove_player(player_name):
    with connection:
        cur.execute("DELETE FROM soccer WHERE player_name = ?", (player_name,))

# Updates medals
def update_medals(player_name, medals):
    with connection:
        cur.execute("""UPDATE soccer SET
                    medals = ? WHERE player_name = ?""", (medals, player_name))

# Inserts a new player
def insert_player(col):
    with connection:
        cur.execute("""INSERT INTO soccer
                    VALUES(?,?,?,?,?,?,?)""", (col[0],col[1],col[2],col[3],col[4],col[5],col[6]))

# Find player by name
def find_player(player_name):
    with connection:
        cur.execute("SELECT * FROM soccer WHERE player_name =?", (player_name,))
        print(cur.fetchone())


connection.close()
#null, integer, real, text, blob
