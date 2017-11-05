from pyquery import PyQuery as pq
from pathlib import Path
from ad import Ad
import re

class Page:
    def __init__(self, number):
        self.number = number
        self.content = None

    def has_next_page(self):
        return self.number < 101

    def get_next_page(self):
        return Page(self.number + 1)

    def get_url(self):
        if (self.number == 1):
            return 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/' \
                   'c37l1700281r15.0?ad=offering&price=550__800&minNumberOfImages=1'
        else:
            return 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/page-%s/' \
                   'c37l1700281r15.0?ad=offering&price=550__800&minNumberOfImages=1' % self.number

    def load_full(self):
        cache_file = Path(self.get_cache_filename())
        if not cache_file.is_file():
            self.content = pq(url=self.get_url())
            self.save_cache(self.content)
        else:
            self.content = self.load_cache()

    def get_cache_filename(self):
        filename = str(self.number) + '.html'
        return "C:\\Users\\2e3s\\PycharmProjects\\rentkijiji\\cache\\pages\\" + filename

    def load_cache(self):
        with open(self.get_cache_filename(), 'r', encoding='utf-8') as content_file:
            content = content_file.read()
            content_file.close()
            return pq(content)

    def save_cache(self, content: pq):
        with open(self.get_cache_filename(), 'w+', encoding='utf-8') as f:
            print(content.html(), file=f)
            f.close()

    def get_ads(self):
        results = self.content('.container-results').find('.search-item')
        ads = []
        for result in results:
            preview = pq(result)
            ads.append(Ad(preview))
        return ads

    def get_results_number(self):
        mp = self.content('.container-results')
        showing = re.search('sur (.+) annon', mp.find('.showing').text()).group(1)
        showing = re.sub('[^0-9]', '', showing)
        return int(showing)
