import os
from typing import List, Tuple, Optional
from pyquery import PyQuery as pq, PyQuery
from pathlib import Path
from requests.exceptions import ChunkedEncodingError
from metro import Metro
import re
from unidecode import unidecode
import datetime


class RetryAdException(Exception):
    pass


class AdPreview:
    _regex_id = re.compile(r"(\d+)\D*$")

    def __init__(self, link: str) -> None:
        if 'en_CA' not in link:
            self.url = link + '?siteLocale=en_CA'
        else:
            self.url = link

        id_match = AdPreview._regex_id.search(link)
        if id_match:
            self.id = id_match.group(1)
        else:
            raise

    def load_full(self) -> PyQuery:
        os.makedirs(self._get_cache_directory(), exist_ok=True)
        cache_file = Path(self._get_cache_filename())
        if not cache_file.is_file():
            try:
                content = pq(url=self.url, headers={'Accept-Language': 'en'})
            except ChunkedEncodingError:
                raise RetryAdException('Refetching ad {}'.format(self.url))
            content.remove('script')
            self._save_cache(content)
        else:
            content = self._load_cache()
        return content

    def _get_cache_directory(self) -> str:
        return "cache/subpages/{}".format(self.id[-2:])

    def _get_cache_filename(self) -> str:
        return "{}/{}".format(self._get_cache_directory(), self.id + '.html')

    def _load_cache(self) -> PyQuery:
        with open(self._get_cache_filename(), 'r', encoding='utf-8') as content_file:
            return pq(content_file.read())

    def _save_cache(self, content: pq) -> None:
        with open(self._get_cache_filename(), 'w+', encoding='utf-8') as f:
            print(content.html(), file=f)
            f.close()

    def clean_cache(self) -> None:
        cache_file = Path(self._get_cache_filename())
        cache_file.unlink(True)


class Ad:
    _regex_text = re.compile(r"[^\w\s]+", re.IGNORECASE)

    def __init__(self, preview: AdPreview) -> None:
        self.url = preview.url
        self.id = preview.id
        self.content = preview.load_full()
        self.cached_text: Optional[str] = None
        self._description: Optional[str] = None
        self._coord: Optional[Tuple[float, float]] = None
        self._closest_metro: Optional[Metro] = None

    def get_id(self) -> str:
        return self.id

    def get_url(self) -> str:
        return self.url

    def get_coord(self) -> Tuple[float, float]:
        if self._coord is None:
            latitude = self.content("meta[property='og:latitude']").attr("content")
            longitude = self.content("meta[property='og:longitude']").attr("content")
            self._coord = float(latitude), float(longitude)
        return self._coord

    def closest_metro(self) -> Metro:
        if self._closest_metro is None:
            self._closest_metro = Metro.get_closest(self.get_coord())
        return self._closest_metro

    def get_title_components(self) -> List[str]:
        # GRAND 3 ½ - UdeM, HEC, HOPITAL – Semi-meublé | 3 1/2 | Ville de Montréal | Kijiji
        title = self.content("meta[property='og:title']").attr("content")
        if title is None:
            raise RetryAdException('No title found in ad {}'.format(self.url))
        titles: List[str] = title.split('|')
        return list(map(lambda x: x.strip(), titles))

    def bedrooms_count(self) -> int:
        container = self.content('[class^=unitRow-]')
        container = container('[class^=titleAttributes-]')
        match = re.search('Bedrooms: (\\d+)', container.text())
        if match:
            return int(match.group(1))
        else:
            raise

    def _has_price(self) -> bool:
        price = str(self.content('[class^=currentPrice-]').text())
        return price.strip().lower() != 'please contact'

    def get_price(self) -> int:
        price = re.sub('\\D', '', self.content('[class^=currentPrice-]').text())
        return int(price) if self._has_price() else -1

    def get_description(self) -> str:
        if self._description is None:
            self._description = str(self.content('*[class^="descriptionContainer-"]').text())
        return self._description

    def is_washer_mentioned(self) -> bool:
        text = self._get_adapted_text()
        has_washer = 'laveuse' in text or 'washer' in text
        has_laundry = 'buanderie' in text \
                      or 'laundry' in text \
                      or 'pas laveuse' in text

        return has_washer and not has_laundry

    def _get_adapted_text(self) -> str:
        if self.cached_text is None:
            cached_text = unidecode(self.get_description()).lower()
            cached_text += unidecode(self.get_title_components()[0]).lower()
            cached_text = re.sub('\\s+', ' ', cached_text)
            self.cached_text = Ad._regex_text.sub('', cached_text)

        return self.cached_text

    def is_basement(self) -> bool:
        text = self._get_adapted_text()
        return 'basement' in text \
               or 'sous so' in text \
               or 'sousso' in text \
               or 'demisol' in text \
               or 'demi sol' in text \
               or 'bachelor' in text

    def get_score(self) -> int:
        metro = self.closest_metro()
        metro_score = metro.score
        distance_score = 100 - int(round(metro.distance() / 10))
        washer_score = 50 if self.is_washer_mentioned() else 0
        room_score = (self.bedrooms_count() - 2) * 100
        price_score = int((1900 - self.get_price()) / 10)
        first_floor_score = 100 if self.is_first_floor() else 0
        last_floor_score = -50 if self.is_last_floor() else 0

        return metro_score * 2 \
            + distance_score \
            + washer_score \
            + room_score \
            + price_score \
            + first_floor_score \
            + last_floor_score

    def is_first_floor(self) -> bool:
        match1 = re.search('rez[\\s-]?de[\\s-]?chauss', self.get_description())
        match2 = re.search('first floor', self.get_description())
        match3 = re.search('1(st)? floor', self.get_description())

        return match1 is not None or match2 is not None or match3 is not None

    def is_last_floor(self) -> bool:
        match1 = re.match('derniere? [eé]tage', self.get_description())
        match2 = re.match('last floor', self.get_description())
        match3 = re.match('(third|3rd) floor', self.get_description())

        return match1 is not None or match2 is not None or match3 is not None

    def get_posted_date(self) -> str:
        date = self.content('*[class^="datePosted-"]').find('time').attr('datetime')
        if date is None:
            raise
        return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z').isoformat(' ')

    def is_nothing_included(self) -> bool:
        text = self._get_adapted_text()
        return 'nothing included' in text \
               or 'nonfurnish' in text \
               or 'non furnish' in text \
               or 'aucune inclu' in text \
               or 'rien inclu' in text \
               or 'rien dinclu' in text
