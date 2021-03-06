from page import Page
from time import sleep
from csv_writer import CsvWriter
from db import Db
from counter import Counter
from ad_validator import AdValidator
import os, errno


def print_both(text, f):
    print(text)
    print(text, file=f)


try:
    os.makedirs('cache/pages')
    os.makedirs('cache/subpages')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


descriptions = dict()

page = Page(1)

f = open("cache/result.txt", 'w+', encoding='utf-8')
counter = Counter(f)
csv_writer = CsvWriter()
csv_writer.init()
db = Db()

while page.has_next_page():
    page.load_full()
    for ad in page.get_ads():
        counter.increase_all()
        if ad.is_montreal():
            ad.load_full()
        else:
            continue

        validator = AdValidator(ad, counter, descriptions)

        if not validator.validate():
            continue

        print_both(ad.get_url(), f)
        print_both(ad.get_title_components() + [ad.get_price()], f)
        if ad.is_washer_mentioned():
            print_both('Washer is mentioned!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', f)
        print(ad.get_description(), file=f)
        print('-----------------------------', file=f)
        print_both('Distance to %s: %s meters' % (ad.get_closest_station()[0], ad.get_closest_station()[1]), f)
        print_both("", f)
        csv_writer.write_csv(ad)
        db.insert(ad)
        sleep(0.1)

    print('\nFetching page %s...\n' % str(page.number + 1))
    page = page.get_next_page()

counter.print()

f.close()
csv_writer.finish()
db.finish()
