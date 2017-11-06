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
                postedTime INTEGER,
                price INTEGER,
                rooms TEXT,
                isNothingIncluded BOOLEAN,
                score INTEGER,
                isLate BOOLEAN,
                isBasement BOOLEAN,
                isWasherMentioned BOOLEAN,
                closestMetro TEXT,
                closestMetroDistance INTEGER
            )
        ''')
        self.db.commit()

    def insert(self, ad: Ad):
        cursor = self.db.cursor()
        cursor.execute('''REPLACE INTO ads(
            id,
            title,
            url,
            description,
            postedTime,
            price,
            rooms,
            isNothingIncluded,
            score,
            isLate,
            isBasement,
            isWasherMentioned,
            closestMetro,
            closestMetroDistance
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
            ad.get_id(),
            ad.get_title_components()[0],
            ad.get_url(),
            ad.get_description(),
            int(datetime.strptime(ad.get_posted_date(), '%Y-%m-%d %H:%M:%S').timestamp()),
            ad.get_price(),
            ad.get_size(),
            ad.is_nothing_included(),
            ad.get_score(),
            ad.is_too_late(),
            ad.is_basement(),
            ad.is_washer_mentioned(),
            ad.get_closest_station()[0],
            ad.get_closest_station()[1]
        ))
        self.db.commit()

    def finish(self):
        self.db.close()
