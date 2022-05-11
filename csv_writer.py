import csv
from typing import Optional, IO, Any
from ad import Ad


class CsvWriter:
    def __init__(self) -> None:
        self.csvFile: Optional[IO[str]] = None
        self.writer: Optional[csv.DictWriter[str]] = None

    def __enter__(self) -> 'CsvWriter':
        self.csvFile = open('cache/result.csv', 'w', newline='',
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
        return self

    def write_csv(self, ad: Ad) -> None:
        if self.writer:
            metro = ad.closest_metro()
            self.writer.writerow({
                'id': ad.get_id(),
                'url': ad.get_url(),
                'has_washer': 'yes' if ad.is_washer_mentioned() else 'no',
                'metro station': metro.name,
                'metro distance': metro.distance(),
                'title': ad.get_title_components()[0],
                'score': ad.get_score(),
                'price': ad.get_price(),
                'date': ad.get_posted_date()
            })

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.csvFile:
            self.csvFile.close()
