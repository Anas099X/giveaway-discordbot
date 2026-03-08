import psycopg2 as postsql
from dotenv import load_dotenv
import os

load_dotenv()


db = postsql.connect(
  host=os.getenv("HOST"),
  user=os.getenv("USER"),
  password=os.getenv("PASSWORD"),
  database=os.getenv("DATABASE"),
  port=os.getenv("PORT")
)
db_cursor = db.cursor()

db_cursor.execute('CREATE TABLE IF NOT EXISTS giveaways (name TEXT PRIMARY KEY, entries TEXT[], winners INTEGER, end_time TIMESTAMP, channel_id BIGINT, message_id BIGINT)')
db.commit()
class Giveaway:
    
    def __init__(self):
     self = None

    def create(self, name, entries, winners, end_time, channel_id, message_id):
      db_cursor.execute(f'INSERT INTO giveaways (name, entries, winners, end_time, channel_id, message_id) VALUES (%s, %s, %s, %s, %s, %s)', (name, entries, winners, end_time, channel_id, message_id))
      db.commit()    

    def delete(self, name):
      db_cursor.execute(f'DELETE FROM giveaways WHERE name = %s', (name,))
      db.commit()

    def update(self, name, field, value):
      db_cursor.execute(f'UPDATE giveaways SET {field} = %s WHERE name = %s', (value, name))
      db.commit()

    def get_one(self, name, filters=None): 
      db_cursor.execute(f'SELECT * FROM giveaways WHERE name = %s', (name,))
      return db_cursor.fetchall()
    
    def get_all(self, filters=None): 
      db_cursor.execute(f'SELECT * FROM giveaways')
      return db_cursor.fetchall()

#giveaway_id = create_giveaway("balls", ["entry1", "entry2"], 1, "2024-06-30 12:00:00")

#giveaway = Giveaway("balls")

#db_cursor.execute("DROP TABLE giveaways")
#db.commit()

#print(giveaway.update("winners", 200))
