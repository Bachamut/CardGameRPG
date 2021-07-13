import pygame

from random import sample
from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.game_logic import GameLogic

CARD_VIEW_ON_RISE = pygame.event.custom_type()
CARD_VIEW_ON_FALL = pygame.event.custom_type()


class CardModel(GameObject):

    _initialized = False

    def __init__(self):
        super(CardModel, self).__init__()


        self.onboard_cards = list()

    def _initialize(self):
        CardModel._initialized = True
        print("CardModel initialized")

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self.current_character = _battle_logic.current_character
        self.current_card = _battle_logic.current_card
        self.selected_card = _battle_logic.selected_card
        self.selected_card_index = 0

        self.previous_character = self.current_character

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
                character.battledeck.append(card_instance)
        # creating draw_pile that is used in battle mode
        character.draw_pile = sample(character.battledeck, len(character.battledeck))

    @staticmethod
    def draw_card(character):
        card = character.draw_pile.pop(0)
        character.hand.append(card)
        character.hand[0].selected = True

    @staticmethod
    def draw_hand(character):
        for it in range(0, character.card_draw):
            CardModel.draw_card(character)

    def on_script(self):
        if not self._initialized and \
            GameLogic._initialized and \
            BattleLogic._initialized and \
            CharacterModel._initialized and \
            BattleLogic.started:
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
                self._card_selection(event)
        pass

    def on_signal(self, signal):
        if CardModel._initialized:
            if signal.type == BattleLogic.CURRENT_CHARACTER_SIGNAL:

                _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

                _card_view = GameObject.get_object_pool().select_with_label("CardView")[0]
                self.previous_character = _card_view.previous_character

                print(f'card_model current_character: {self.current_character.take().name}')

                self.selected_card_index = 0

                for card in self.previous_character.take().hand:
                    card.selected = False
                    card.current = False

                self.current_character.take().hand[0].selected = True
                
                signal = pygame.event.Event(CARD_VIEW_ON_FALL, {'event': 'CARD_VIEW_ON_FALL'})
                pygame.event.post(signal)

                signal = pygame.event.Event(CARD_VIEW_ON_RISE, {'event': 'CARD_VIEW_ON_RISE'})
                pygame.event.post(signal)

        pass

    def _on_arrow_right(self, event):
        if event.key == pygame.K_RIGHT:

            _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

            if self.selected_card_index < len(self.current_character.take().hand) - 1:
                self.current_character.take().hand[self.selected_card_index].selected = False
                self.selected_card_index += 1
                print(f'{self.selected_card_index}')
                self.current_character.take().hand[self.selected_card_index].selected = True

                # Current Card to Info View

    def _on_arrow_left(self, event):
        if event.key == pygame.K_LEFT:
            if self.selected_card_index > 0:

                _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

                self.current_character.take().hand[self.selected_card_index].selected = False
                self.selected_card_index -= 1
                print(f'{self.selected_card_index}')
                self.current_character.take().hand[self.selected_card_index].selected = True

                # Current Card to Info View

    def _card_selection(self, event):
        if event.key == pygame.K_RETURN:

            _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

            BattleLogic.current_card.update(self.current_character.take().hand[self.selected_card_index])
            BattleLogic.current_card.take().current = True
            print(f'wybrana karta: {BattleLogic.current_card.take().card_name}')

            BattleLogic.card_model_active = False

            signal = pygame.event.Event(BattleLogic.CURRENT_CARD_SIGNAL, {"event": "CURRENT_CARD_SIGNAL"})
            pygame.event.post(signal)
