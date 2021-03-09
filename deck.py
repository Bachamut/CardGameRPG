class InvalidDeckSizeException(Exception):
    pass


class Deck(list):

    def __init__(self, min_deck, max_deck):
        super(Deck, self).__init__()
        self.min_deck = min_deck
        self.max_deck = max_deck
        self.card_pool = []

    def confirm_deck(self):
        if self.min_deck < len(self) < self.max_deck:
            return self
        else:
            raise InvalidDeckSizeException("Invalid Deck Size Exception")

    def append(self, card):
        return list.append(self, card)

    def add_card(self, card):
        self.card_pool.remove(card)
        self.append(card)

    def remove_card(self, card):
        self.remove(card)
        self.card_pool.append(card)

