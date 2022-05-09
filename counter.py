from typing import IO


class Counter:
    def __init__(self, file_pointer: IO[str]) -> None:
        self.file_pointer = file_pointer
        self.counter_non_montreal = 0
        self.counter_too_far = 0
        self.counter_non_size = 0
        self.counter_basement = 0
        self.counter_duplicates = 0
        self.counter_too_late = 0
        self.counter_nothing_included = 0
        self.counter_all = 0

    def increase_all(self) -> None:
        self.counter_all += 1

    def too_far(self) -> None:
        self.counter_too_far += 1

    def wrong_size(self) -> None:
        self.counter_non_size += 1

    def basement(self) -> None:
        self.counter_basement += 1

    def duplicate(self) -> None:
        self.counter_duplicates += 1

    def too_late(self) -> None:
        self.counter_too_late += 1

    def nothing_included(self) -> None:
        self.counter_nothing_included += 1

    def print_both(self, text: str) -> None:
        print(text)
        print(text, file=self.file_pointer)

    def print(self) -> None:
        self.print_both('Filtered non-Montreal: %s' % self.counter_non_montreal)
        self.print_both('Filtered too far from metro: %s' % self.counter_too_far)
        self.print_both('Filtered non-size: %s' % self.counter_non_size)
        self.print_both('Filtered basements: %s' % self.counter_basement)
        self.print_both('Filtered duplicates: %s' % self.counter_duplicates)
        self.print_both('Filtered too late: %s' % self.counter_too_late)
        self.print_both('Filtered nothing included: %s' % self.counter_nothing_included)
        self.print_both('Total: %s' % self.counter_all)
