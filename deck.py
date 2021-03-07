class Deck():

    def add_card(self, card_info):

        self.deck_cards = []
        self.deck_cards.append(card_info)

        print(self.deck_cards)

    def get_deck(self):
        for card in self.deck_cards:
            print(card)
            # for key, value in self.deck_cards.items():
            #     print(key + " : " + value)



