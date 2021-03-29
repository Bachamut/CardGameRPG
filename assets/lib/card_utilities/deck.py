
class InvalidDeckSizeException(Exception):
    pass


class Deck(dict):

    def __init__(self, min_size=-1, max_size=-1):
        super(Deck, self).__init__()
        self.min_size = min_size
        self.max_size = max_size

    def confirm_deck(self):
        if self.min_size < len(self) < self.max_size:
            return self
        else:
            raise InvalidDeckSizeException("Invalid Deck Size Exception")
