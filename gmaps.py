import sqlite3
import configparser
import googlemaps
from datetime import datetime, timedelta


class Coordinate:
    def __init__(self, latitude, longitude, toMetro, toWork):
        self.latitude = latitude
        self.longitude = longitude
        self.toMetro = toMetro
        self.toWork = toWork


class GMaps:
    def __init__(self):
        self.db = sqlite3.connect('coordinates.db')
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coordinates(
                latitude REAL,
                longitude REAL,
                toMetro INTEGER,
                toWork INTEGER
            )
        ''')
        self.db.commit()
        config = configparser.ConfigParser()
        config.read("settings.ini")
        apikey = config.get('Default', 'apikey')
        self.gmaps = googlemaps.Client(key=apikey)

    def insert(self, latitude, longitude, toMetro, toWork):
        cursor = self.db.cursor()
        cursor.execute('''INSERT INTO coordinates(
            latitude,
            longitude,
            toMetro,
            toWork
            ) VALUES(?,?,?,?)''', (latitude, longitude, toMetro, toWork))
        self.db.commit()

    def get_coordinates(self):
        cursor = self.db.cursor()
        cursor.execute('''SELECT latitude, longitude, toMetro, toWork FROM coordinates''')
        result = []
        for point in cursor:
            result.append(Coordinate(point[0], point[1], point[2], point[3]))
        return result

    def finish(self):
        self.db.close()

    def _get_transit_time(self, point1: tuple, point2: tuple):
        today_date = datetime.now().strftime('%Y-%m-%d 09:00:00')
        date = datetime.strptime(today_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        time = date.timestamp()
        self.gmaps.directions(str(point1[0]) + ' ' + str(point1[1]),
                              str(point2[0]) + ' ' + str(point2[1]),
                              units='metric',
                              mode="transit",
                              departure_time=time)

    def _get_foot_time(self, point1: tuple, point2: tuple):
        today_date = datetime.now().strftime('%Y-%m-%d 09:00:00')
        date = datetime.strptime(today_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        time = date.timestamp()
        self.gmaps.directions(str(point1[0]) + ' ' + str(point1[1]),
                              str(point2[0]) + ' ' + str(point2[1]),
                              units='metric',
                              mode="transit",
                              departure_time=time)
