import sqlite3
from typing import Union, Any, Iterable

from ad import Ad, AdPreview
from datetime import datetime


class AdStorage:
    def __init__(self) -> None:
        self.current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    def __enter__(self) -> None:
        self.connection = sqlite3.connect('cache/result.db')
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ads(
                id INTEGER PRIMARY KEY,
                title TEXT,
                url TEXT,
                description TEXT,
                postedTime INTEGER,
                price INTEGER,
                bedrooms INTEGER,
                isNothingIncluded BOOLEAN,
                score INTEGER,
                isLate BOOLEAN,
                isBasement BOOLEAN,
                isWasherMentioned BOOLEAN,
                closestMetro TEXT,
                closestMetroDistance INTEGER,
                isRemoved BOOLEAN,
                createdAt timestamp DEFAULT CURRENT_TIMESTAMP,
                hasFloor INTEGER DEFAULT 0
            )
        ''')
        self.connection.commit()

    def insert(self, ad: Ad) -> None:
        if self.has_ad(ad):
            cursor = self.connection.cursor()
            cursor.execute('SELECT createdAt, isRemoved FROM ads WHERE id = ?', (ad.id,))
            row = cursor.fetchone()
            created_at = str(row[0])
            is_removed = int(row[1])
        else:
            created_at = self.current_time
            is_removed = 0

        cursor = self.connection.cursor()
        cursor.execute('''REPLACE INTO ads(
            id,
            title,
            url,
            description,
            postedTime,
            price,
            bedrooms,
            isNothingIncluded,
            score,
            isBasement,
            isWasherMentioned,
            closestMetro,
            closestMetroDistance,
            hasFloor,
            isRemoved,
            createdAt
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
            ad.id,
            ad.get_title_components()[0],
            ad.url,
            ad.get_description(),
            int(datetime.strptime(ad.get_posted_date(), '%Y-%m-%d %H:%M:%S').timestamp()),
            ad.get_price(),
            ad.bedrooms_count(),
            ad.is_nothing_included(),
            ad.get_score(),
            ad.is_basement(),
            ad.is_washer_mentioned(),
            ad.closest_metro().name,
            ad.closest_metro().distance(),
            -1 if ad.is_last_floor() else (1 if ad.is_first_floor() else 0),
            is_removed,
            created_at,
        ))
        self.connection.commit()

    def has_ad(self, ad: Union[Ad, AdPreview]) -> bool:
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM ads WHERE id = ?', (ad.id,))
        count = int(cursor.fetchone()[0])
        return count != 0

    def get_ad_previews(self) -> Iterable[AdPreview]:
        cursor = self.connection.cursor()
        cursor.execute('SELECT url FROM ads')
        rows = cursor.fetchall()
        for row in rows:
            yield AdPreview(row[0])

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.connection.close()
