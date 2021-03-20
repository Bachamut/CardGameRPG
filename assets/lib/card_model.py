from random import sample

import pygame

from assets.lib.battle_logic import BattleLogic
from assets.lib.card_manager import CardManager
from assets.lib.character_model import CharacterModel
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class CardModel(GameObject):

    _initialized = False
    active = BattleLogic.card_model_active
    onboard_cards = []
    selected_card = 0

    def __init__(self):
        super(CardModel, self).__init__()
        self.character = None

    def _initialize(self):
        CardModel._initialized = True
        self.character = BattleLogic.current_character

    def on_create(self):
        self.position = self.property('TransformProperty').position
        self.position.y = 576
        self.position.x = 24

    @staticmethod
    def create_battledeck(character):

        for card, amount in character.deck.items():
            for it in range(0, amount):
                card_instance = CardManager.create_card(card)

                card_instance.object_class = 'Card'
                card_instance.object_type = 'Card'
                card_instance.object_label = card_instance.card_name
                card_instance.add_property('TransformProperty')
                card_instance.add_property('BlitProperty')
                card_instance.add_property('SpriteProperty')
                card_instance.add_property('TranslateProperty')
                card_instance.property('SpriteProperty').set_resource(CardManager.card_config[card]['resource'])
                card_instance.property('SpriteProperty').visible = False
                card_instance.on_create()

                GameObject.add_new_object(card_instance)
                # CardModel.onboard_cards.append(card_instance)

                character.battledeck.append(card_instance)
        # creating draw_pile that is used in battle mode
        character.draw_pile = sample(character.battledeck, len(character.battledeck))

    @staticmethod
    def draw_card(character):
        card = character.draw_pile.pop(0)
        character.hand.append(card)
        # zrobić opuszczanie kart poprzednio wybranych
        character.hand[0].selected = True

    @staticmethod
    def draw_hand(character):
        for it in range(0, character.card_draw):
            CardModel.draw_card(character)

    def on_script(self):
        if not self._initialized and GameLogic._initialized and BattleLogic._initialized and CharacterModel._initialized and BattleLogic.started:
            self._initialize()
        else:
            pass

        if BattleLogic.card_model_active:
            pass

    def on_event(self, event):
        if BattleLogic.card_model_active and CardModel._initialized:

            if event.type == pygame.KEYDOWN:
                self._on_arrow_right(event)
                self._on_arrow_left(event)
        pass

    def _on_arrow_right(self, event):
        if event.key == pygame.K_RIGHT:
            # CharacterView.current_character -> BattleLogic.current_character
            if CardModel.selected_card < len(self.character.hand) - 1:
                self.character.hand[CardModel.selected_card].selected = False
                CardModel.selected_card += 1
                print(f'{self.selected_card}')
                self.character.hand[CardModel.selected_card].selected = True

    def _on_arrow_left(self, event):
        if event.key == pygame.K_LEFT:
            if CardModel.selected_card > 0:
                self.character.hand[CardModel.selected_card].selected = False
                CardModel.selected_card -= 1
                print(f'{self.selected_card}')
                self.character.hand[CardModel.selected_card].selected = True
