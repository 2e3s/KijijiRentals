#!venv/bin/python3

from argparse import ArgumentParser
from typing import Dict, IO, Any
from ad import Ad, RetryAdException, AdPreview
from feed import Feed
from page import PageLoader
from time import sleep
from csv_writer import CsvWriter
from db import AdStorage
from counter import Counter
from ad_validator import AdValidator
import os
import errno


def print_both(text: Any, file: IO[str]) -> None:
    print(text)
    print(text, file=file)


def process_ad(_ad_preview: AdPreview) -> bool:
    counter.increase_all()

    if ad_storage.has_ad(_ad_preview):
        print_both('Ad {} is already parsed\n'.format(_ad_preview.id), f)
        return False

    attempt = 0
    while True:
        try:
            adv = Ad(_ad_preview)
            ad_storage.insert(adv)
            break
        except RetryAdException as e:
            attempt += 1
            print_both('!!!!!!!!!' + repr(e) + '!!!!!!!!!', f)
            if attempt >= 5:
                print_both('!!!!!!!!!Ad is broken: {}!!!!!!!!!'.format(_ad_preview.url), f)
                return True
            _ad_preview.clean_cache()
        sleep(5)

    validator = AdValidator(adv, counter, descriptions)
    if not validator.validate():
        print_both("", f)
        return True
    print_both(adv.url, f)
    print_both(adv.get_title_components() + [str(adv.get_price())], f)
    if adv.is_washer_mentioned():
        print_both('Washer is mentioned', f)
    print(adv.get_description(), file=f)
    print('-----------------------------', file=f)
    print_both('Distance to %s: %s meters' % (
        adv.closest_metro().name,
        adv.closest_metro().distance()
    ), f)
    print_both("", f)
    csv_writer.write_csv(adv)

    return True


try:
    os.makedirs('cache/pages')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

descriptions: Dict[str, bool] = dict()

f = open("cache/result.txt", 'w+', encoding='utf-8')
counter = Counter(f)
csv_writer = CsvWriter()
ad_storage = AdStorage()

parser = ArgumentParser(description="Kijiji rentals parser")
parser.add_argument("--rss", action='store_true', help="Parse RSS feed")
parser.add_argument("--pages", type=int, default=5, help="How many pages to go through")
args = parser.parse_args()

with csv_writer, ad_storage:
    if args.rss:
        print_both('Parsing RSS...', f)
        for (ad_preview, point) in Feed().load_ads():
            if not AdValidator.validate_coordinate(point, counter):
                continue
            if process_ad(ad_preview):
                sleep(0.1)
    else:
        print_both('Loading {} pages'.format(args.pages), f)
        page_loader = PageLoader(args.pages)

        for loaded_page in page_loader.fetch():
            for ad_preview in loaded_page.get_ads():
                if process_ad(ad_preview):
                    sleep(0.1)
            sleep(1)
            print('\nFetching page %s...\n' % str(loaded_page.number + 1))

counter.print()

f.close()
