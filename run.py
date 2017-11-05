from page import Page
from time import sleep
from csv_writer import CsvWriter
from db import Db
from counter import Counter


def print_both(text, f):
    print(text)
    print(text, file=f)


descriptions = dict()

page = Page(1)
counter_non_montreal = 0
counter_too_far = 0
counter_all = 0
counter_non_size = 0
counter_basement = 0
counter_duplicates = 0
counter_too_late = 0

f = open("C:\\Users\\2e3s\\PycharmProjects\\rentkijiji\\cache\\result.txt", 'w+', encoding='utf-8')
counter = Counter(f)
csv_writer = CsvWriter()
csv_writer.init()
db = Db()

while page.has_next_page():
    page.load_full()
    for ad in page.get_ads():
        counter.increase_all()
        if ad.is_montreal():
            counter.non_montreal()
            continue
        ad.load_full()

        if ad.get_description() in descriptions:
            counter.duplicate()
            continue
        else:
            descriptions[ad.get_description()] = True

        if ad.get_closest_station()[1] > 1000:
            counter.too_far()
            continue

        if ad.get_size() != '3 1/2' and ad.get_size() != '4 1/2':
            counter.wrong_size()
            continue

        if ad.is_basement():
            counter.basement()
            continue

        if ad.is_too_late():
            counter.too_late()
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
