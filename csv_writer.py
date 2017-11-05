import csv
from ad import Ad

class CsvWriter:
    def __init__(self):
        self.csvFile = None
        self.writer = None

    def init(self):
        self.csvFile = open('C:\\Users\\2e3s\\PycharmProjects\\rentkijiji\\cache\\result.csv', 'w', newline='',
                            encoding='utf-8')
        self.writer = csv.DictWriter(self.csvFile, fieldnames=[
            'id',
            'url',
            'has_washer',
            'metro station',
            'metro distance',
            'title',
            'score',
            'price',
            'date'
        ])
        self.writer.writeheader()

    def write_csv(self, ad: Ad):
        metro = ad.get_closest_station()
        self.writer.writerow({
            'id': ad.get_id(),
            'url': ad.get_url(),
            'has_washer': 'yes' if ad.is_washer_mentioned() else 'no',
            'metro station': metro[0],
            'metro distance': metro[1],
            'title': ad.get_title_components()[0],
            'score': ad.get_score(),
            'price': ad.get_price(),
            'date': ad.get_posted_date()
        })

    def finish(self):
        self.csvFile.close()
