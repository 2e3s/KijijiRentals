from pyquery import PyQuery as pq
from pathlib import Path
from geopy.distance import vincenty
from metro import Metro
import re
from unidecode import unidecode


class Ad:
    _regex = re.compile(r"[^\w\s]+", re.IGNORECASE)

    def __init__(self, preview: pq):
        self.preview = preview
        self.content = None
        self.cached_text = None

    def is_montreal(self):
        location = self.preview.find('.location').remove('span').text()
        return location != 'Ville de Montréal'

    def get_id(self):
        return self.preview.attr('data-ad-id')

    def get_url(self):
        return 'https://www.kijiji.ca' + self.preview.attr('data-vip-url')

    def load_full(self):
        cache_file = Path(self.get_cache_filename())
        if not cache_file.is_file():
            self.content = pq(url=self.get_url())
            self.save_cache(self.content)
        else:
            self.content = self.load_cache()

    def get_cache_filename(self):
        filename = self.get_id() + '.html'
        return "C:\\Users\\2e3s\\PycharmProjects\\rentkijiji\\cache\\subpages\\" + filename

    def load_cache(self):
        with open(self.get_cache_filename(), 'r', encoding='utf-8') as content_file:
            return pq(content_file.read())

    def save_cache(self, content: pq):
        with open(self.get_cache_filename(), 'w+', encoding='utf-8') as f:
            print(content.html(), file=f)
            f.close()

    def get_coord(self):
        latitude = self.content("meta[property='og:latitude']").attr("content");
        longitude = self.content("meta[property='og:longitude']").attr("content");
        return float(latitude), float(longitude)

    def get_closest_station(self):
        i = 0
        min_distance = 10000000000
        metro_index = 0
        for metro in Metro.stations:
            lat = metro[0]
            lon = metro[1]
            name = metro[2]
            distance = vincenty((lat, lon), self.get_coord()).meters
            if distance < min_distance:
                min_distance = distance
                metro_index = i
            i += 1

        return Metro.stations[metro_index][2], round(min_distance), metro_index

    def get_closest_station_distance(self):
        metro = self.get_closest_station()
        return round(vincenty((metro[0], metro[1]), self.get_coord()).meters)

    def get_title_components(self):
        # GRAND 3 ½ - UdeM, HEC, HOPITAL – Semi-meublé | 3 1/2 | Ville de Montréal | Kijiji
        titles = self.content("meta[property='og:title']").attr("content").split('|')

        return list(map(lambda x: x.strip(), titles))

    def get_size(self):
        return self.get_title_components()[1]

    def get_price(self):
        price = re.search('^\d+', self.preview('.price').text()).group(0)
        return int(price)

    def get_description(self):
        return self.content('*[class^="descriptionContainer-"]').text()

    def is_washer_mentioned(self):
        text = self._get_adapted_text()
        has_washer = 'laveuse' in text or 'washer' in text
        has_laundry = 'buanderie' in text \
                      or 'laundry' in text \
                      or 'pas laveuse' in text

        return has_washer and not has_laundry

    def _get_adapted_text(self):
        text = unidecode(self.get_description()).lower()
        text += unidecode(self.get_title_components()[0]).lower()
        text = re.sub()
        return text

    def is_basement(self):
        text = self._get_adapted_text()
        return 'basement' in text \
               or 'sous so' in text \
               or 'sous-so' in text \
               or 'sousso' in text \
               or 'bachelor' in text

    def is_too_late(self):
        text = self._get_adapted_text()
        has_late = 'janvier' in text \
                   or 'january' in text \
                   or 'fevrier' in text \
                   or 'february' in text

        has_now = 'november' in text or 'novembre' in text

        return has_late and not has_now

    def get_score(self):
        metro = self.get_closest_station()
        metro_score = Metro.stations[metro[2]][3]
        distance_score = int(round(metro[1] / 10))
        washer_score = 50 if self.is_washer_mentioned() else 0

        return metro_score * 2 + (100 - distance_score) + washer_score

    def get_posted_date(self):
        return self.content('*[class^="datePosted-"]').find('time').attr('datetime')
