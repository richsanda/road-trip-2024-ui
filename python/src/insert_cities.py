import sqlite3

# List of cities with state abbreviations
cities = [
    'saratoga springs, ny', 'troy, ny', 'clifton park, ny', 'schenectady, ny',
    'cleveland, oh', 'detroit, mi', 'marquette, mi', 'ashland, wi',
    'superior, wi', 'duluth, mn', 'grand forks, nd', 'devils lake, nd',
    'rugby, nd', 'minot, nd', 'williston, nd', 'culbertson, mt',
    'sidney, mt', 'glasgow, mt', 'malta, mt', 'chinook, mt', 'havre, mt',
    'box elder, mt', 'big sandy, mt', 'fort benton, mt', 'great falls, mt',
    'consul, sk', 'maple creek, sk', 'medicine hat, ab', 'hanna, ab',
    'drumheller, ab', 'calgary, ab', 'nanton, ab', 'cardston, ab',
    'whitefish, mt', 'kalispell, mt', 'missoula, mt', 'helena, mt',
    'bozeman, mt', 'billings, mt', 'broadus, mt', 'deadwood, sd',
    'sturgis, sd', 'hot springs, sd', 'rapid city, sd', 'pierre, sd',
    'sioux city, ia', 'cedar rapids, ia', 'quad cities, ia', 'chicago, il',
    'ann arbor, mi', 'london, on', 'niagra, on', 'buffalo, ny', 'albany, ny',
    'plymouth, ma'
]

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# SQL query to insert into the 'stories' table
insert_query = "INSERT INTO stories (text, category) VALUES (?, ?)"

# Insert each city into the 'stories' table
for city in cities:
    cursor.execute(insert_query, (city, 'cities'))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Cities inserted successfully.")
