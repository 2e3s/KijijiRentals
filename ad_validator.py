from ad import Ad
from counter import Counter

class AdValidator:
    def __init__(self, ad: Ad, counter: Counter, descriptions: dict):
        self.descriptions = descriptions
        self.counter = counter
        self.ad = ad

    def validate(self):
        if not self.ad.is_montreal():
            self.counter.non_montreal()
            return False

        if self.ad.get_description() in self.descriptions:
            self.counter.duplicate()
            return False
        else:
            self.descriptions[self.ad.get_description()] = True

        if self.ad.get_closest_station()[1] > 1000:
            self.counter.too_far()
            return False

        if self.ad.get_size() != '3 1/2' and self.ad.get_size() != '4 1/2':
            self.counter.wrong_size()
            return False

        if self.ad.is_basement():
            self.counter.basement()
            return False

        if self.ad.is_too_late():
            self.counter.too_late()
            return False

        return True
