from typing import Iterable
from pyquery import PyQuery as pq, PyQuery
from pathlib import Path
from ad import AdPreview
import re


class PageLoader:
    def __init__(self, max_number: int) -> None:
        self.max_number = max_number

    def fetch(self) -> Iterable['Page']:
        number = 1
        while number <= self.max_number:
            page = Page(number, self._load_full(number))
            if not page.has_next_page():
                break
            yield page
            number += 1

    @staticmethod
    def _get_url(number: int) -> str:
        if number == 1:
            return 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/' \
                   '4+1+2__4+1+2+et+coin+detente__5+1+2__5+1+2+et+coin+detente__6+1+2/' \
                   'c37l1700281a27949001?ll=45.518721%2C-73.587508&address=Montreal%2C+QC+H2T+2T1' \
                   '&ad=offering&minNumberOfImages=1&price=800__1900&meuble=0&radius=9.0'
        else:
            return 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/' \
                   '4+1+2__4+1+2+et+coin+detente__5+1+2__5+1+2+et+coin+detente__6+1+2/' \
                   'page-{}/c37l1700281a27949001?radius=9.0&ad=offering&price=800__1900' \
                   '&minNumberOfImages=1&address=Montreal%2C+QC+H2T+2T1' \
                   '&ll=45.518721,-73.587508&meuble=0'.format(number)

    def _load_full(self, number: int) -> PyQuery:
        filename = self._get_cache_filename(number)
        cache_file = Path(filename)
        if not cache_file.is_file():
            content = pq(url=self._get_url(number) + '&siteLocale=en_CA')
            self._save_cache(filename, content)
        else:
            content = self._load_cache(filename)
        return content

    @staticmethod
    def _get_cache_filename(number: int) -> str:
        filename = str(number) + '.html'
        return "cache/pages/" + filename

    @staticmethod
    def _load_cache(filename: str) -> PyQuery:
        with open(filename, 'r', encoding='utf-8') as content_file:
            content = content_file.read()
            content_file.close()
            return pq(content)

    @staticmethod
    def _save_cache(filename: str, content: pq) -> None:
        with open(filename, 'w+', encoding='utf-8') as f:
            print(content.html(), file=f)
            f.close()


class Page:
    def __init__(self, number: int, content: PyQuery) -> None:
        self.number = number
        self.content = content

    def has_next_page(self) -> bool:
        return self._results_number() == 0

    def get_ads(self) -> Iterable[AdPreview]:
        results = self.content('.container-results').find('.search-item')
        for result in results:
            yield AdPreview('https://www.kijiji.ca' + pq(result).attr('data-vip-url'))

    def _results_number(self) -> int:
        mp = self.content('.container-results')
        match = re.search('of (\\d+) results', mp.find('[class^=resultsShowingCount-]').text())
        if match:
            return int(match.group(1))
        return 0
