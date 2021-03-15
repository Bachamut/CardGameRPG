from assets.lib.card_manager import CardManager
import random

class BattleLogic():

    # def __init__(self):
        # self.battledeck = []
        # self.hand = []

    @staticmethod
    def create_battledeck(character):
        for card_instance, quantity in character.deck.items():
            for card in range(0, quantity):
                card = CardManager.create_card(card_instance)
                character.battledeck.append(card)

    @staticmethod
    def card_draw(character, draw_pile):
        card = draw_pile.pop(0)
        character.hand.append(card)

    @staticmethod
    def get_hand(character, draw_amount=3):
        draw_pile = random.sample(character.battledeck, len(character.battledeck))
        for draw_card in range(0, draw_amount):
            BattleLogic.card_draw(character, draw_pile)

