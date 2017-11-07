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
            print(self.ad.get_id() + ' is not Montreal...........')
            return False

        if self.ad.get_description() in self.descriptions:
            self.counter.duplicate()
            print(self.ad.get_id() + ' is a duplicate...........')
            return False
        else:
            self.descriptions[self.ad.get_description()] = True

        if self.ad.is_near_work():
            if self.ad.get_closest_station()[1] > 2000:
                self.counter.too_far()
                print(self.ad.get_id() + ' is too far...........')
                return False
        elif self.ad.get_closest_station()[1] > 1000:
            self.counter.too_far()
            print(self.ad.get_id() + ' is too far...........')
            return False

        if not (self.ad.is_one_room() or self.ad.is_two_room()):
            self.counter.wrong_size()
            print(self.ad.get_id() + ' is wrong size: ' + self.ad.get_size() + '...........')
            return False

        if self.ad.is_basement():
            self.counter.basement()
            print(self.ad.get_id() + ' is basement...........')
            return False

        if self.ad.is_too_late():
            self.counter.too_late()
            print(self.ad.get_id() + ' is too late...........')
            return False

        if self.ad.is_nothing_included():
            self.counter.nothing_included()
            print(self.ad.get_id() + ' is nothing included...........')
            return False

        return True
