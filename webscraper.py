import requests
from bs4 import BeautifulSoup
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

# Updates the number of medals for a player
def update_medals(player_name, medals):
    with connection:
        cur.execute("""UPDATE soccer SET
                    medals = ? WHERE player_name = ?""", (medals, player_name))

# Inserts a player
def insert_player(col):
    with connection:
        cur.execute("""INSERT INTO soccer
                    VALUES(?,?,?,?,?,?,?)""", (col[0],col[1],col[2],col[3],col[4],col[5],col[6]))

# Find a player by name and return info
def find_player(player_name):
    with connection:
        cur.execute("SELECT * FROM soccer WHERE player_name =?", (player_name,))
        print(cur.fetchone())



# grab the html and put in soup
url = 'https://en.wikipedia.org/wiki/List_of_Premier_League_winning_players'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
response.close()

# grab the table from the source and then get the rows of the table
table = soup.find("table", attrs={"class": "wikitable sortable plainrowheaders"})
rows=table.tbody.findAll('tr')


# iterate through each row but skip the first row (column titles)
iter_rows = iter(rows)
next(iter_rows)
for row in iter_rows:
    # grab the player name, number of medals, coutnry, position, team, the season
    # that the first medal was awarded, and the season that the last medal
    # was awarded
    # inserts each row into the database
    name = row.th.find('a').text
    other_data = row.findAll('td')
    number_medals = other_data[0].text.strip()
    country = other_data[1].span.a.text
    position = other_data[2].span.text
    team = other_data[3].a.text
    years = other_data[4].findAll('a')
    first_season = years[0].text
    last_season = years[-1].text
    row_data = (name, number_medals, country, position, team, first_season, last_season)
    insert_player(row_data)

player = "Paul Ince"
find_player(player)
connection.close()
