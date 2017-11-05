import sqlite3
from ad import Ad
from datetime import datetime


class Db:
    def __init__(self):
        self.db = sqlite3.connect('C:\\Users\\2e3s\\PycharmProjects\\rentkijiji\\cache\\result.db')
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads(
                id INTEGER PRIMARY KEY,
                title TEXT,
                url TEXT,
                description TEXT,
                postedTime INTEGER
            )
        ''')
        self.db.commit()

    def insert(self, ad: Ad):
        cursor = self.db.cursor()
        cursor.execute('''REPLACE INTO ads(id, title, url, description, postedTime)
                          VALUES(?,?,?,?,?)''', (
            ad.get_id(),
            ad.get_title_components()[0],
            ad.get_url(),
            ad.get_description(),
            int(datetime.strptime(ad.get_posted_date(), '%Y-%m-%dT%H:%M:%S.000Z').timestamp())
        ))
        self.db.commit()

    def finish(self):
        self.db.close()
