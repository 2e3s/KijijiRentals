from typing import Tuple, Dict

from ad import Ad
from counter import Counter
from metro import Metro


class AdValidator:
    def __init__(self, ad: Ad, counter: Counter, descriptions: Dict[str, bool]):
        self.descriptions = descriptions
        self.counter = counter
        self.ad = ad

    @staticmethod
    def validate_coordinate(point: Tuple[float, float], counter: Counter) -> bool:
        station = Metro.get_closest(point)
        if station.distance_to(point) < 1000:
            return True
        counter.too_far()
        return False

    def validate(self) -> bool:
        if self.ad.get_description() in self.descriptions:
            self.counter.duplicate()
            print(self.ad.id + ' is a duplicate...........')
            return False
        else:
            self.descriptions[self.ad.get_description()] = True

        if Metro.get_closest(self.ad.get_coord()).distance() > 1000:
            self.counter.too_far()
            print(self.ad.id + ' is too far...........')
            return False

        if self.ad.bedrooms_count() < 2:
            self.counter.wrong_size()
            print(self.ad.id + ' is too small...........')
            return False

        if self.ad.is_basement():
            self.counter.basement()
            print(self.ad.id + ' is basement...........')
            return False

        if self.ad.is_nothing_included():
            self.counter.nothing_included()
            print(self.ad.id + ' is nothing included...........')
            return False

        return True
