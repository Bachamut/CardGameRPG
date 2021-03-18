from random import random

from assets.lib.battle_logic import BattleLogic
from assets.lib.card_manager import CardManager
from assets.lib.character_model import CharacterModel
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class CardModel(GameObject):

    _initialized = False
    active = BattleLogic.card_model_active

    def __init__(self):
        super(CardModel, self).__init__()
        self.character = BattleLogic.current_character

        self.selected_card = 0

    def _initialize(self):
        CardModel._initialized = True

    def on_create(self):
        self.position = self.property('TransformProperty').position
        self.position.y = 576
        self.position.x = 24

    @staticmethod
    def create_battledeck(character):

        step = 0
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
                card_instance.on_create()

                # przenieść do CardView
                position = card_instance.property('TransformProperty').position
                position.x += step
                step += 128
                position.y = 576

                GameObject.add_new_object(card_instance)
                # CardView.attach_child(card_instance)

                character.battledeck.append(card_instance)

        # character.draw_pile = random.sample(character.battledeck, len(character.battledeck))
        character.draw_pile = character.battledeck

    def draw_card(self):
        card = self.character.draw_pile.pop(0)
        self.character.hand.append(card)
        # zrobić opuszczanie kart poprzednio wybranych
        self.character.hand[0].selected = True

    def draw_hand(self):
        for card in range(0, self.character.card_draw):
            self.draw_card()

    def on_script(self):
        if not self._initialized and GameLogic._initialized and BattleLogic._initialized and CharacterModel._initialized:
            self._initialize()
        else:
            pass

        if BattleLogic.card_model_active:
            pass

        # przenieść do CardView
        # for card in self.character.draw_pile:
        #     if card.selected == True:
        #         position = card.property('TransformProperty').position
        #         position.y = 0
        #     elif card.selected == False:
        #         position = card.property('TransformProperty').position
        #         position.y = 16

    def on_event(self, event):
        if BattleLogic.card_model_active:
            pass
        pass

        # if event.type == pygame.KEYDOWN:
            # self._on_arrow_right(event)
            # self._on_arrow_left(event)

    # def _on_arrow_right(self, event):
    #     if event.key == pygame.K_RIGHT:
    #         # CharacterView.current_character -> BattleLogic.current_character
    #         if self.selected_card < (sum(CharacterView.current_player.deck.values()) - 1):
    #             self.character.hand[self.selected_card].selected = False
    #             self.selected_card += 1
    #             print(f'{self.selected_card}')
    #             self.character.hand[self.selected_card].selected = True
    #
    # def _on_arrow_left(self, event):
    #     if event.key == pygame.K_LEFT:
    #         if self.selected_card > 0:
    #             self.character.hand[self.selected_card].selected = False
    #             self.selected_card -= 1
    #             print(f'{self.selected_card}')
    #             self.character.hand[self.selected_card].selected = True