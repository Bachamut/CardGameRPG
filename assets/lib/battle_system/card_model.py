import pygame

from random import sample
from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.game_logic import GameLogic
from resource_manager.shared_resource import SharedResource
from assets.lib.battle_system.log import Logs

CARD_VIEW_ON_RISE = pygame.event.custom_type()
CARD_VIEW_ON_FALL = pygame.event.custom_type()


class CardModel(GameObject):

    # SharedResources definitions

    @property
    def current_character(self):
        return self._current_character.take()

    @current_character.setter
    def current_character(self, character):
        self._current_character.set(character)

    @property
    def current_target(self):
        return self._current_target.take()

    @current_target.setter
    def current_target(self, character):
        self._current_target.set(character)

    @property
    def selected_target(self):
        return self._selected_target.take()

    @selected_target.setter
    def selected_target(self, target):
        self._selected_target.set(target)

    @property
    def current_card(self):
        return self._current_card.take()

    @current_card.setter
    def current_card(self, card):
        self._current_card.set(card)

    @property
    def selected_card(self):
        return self._selected_card.take()

    @selected_card.setter
    def selected_card(self, card):
        self._selected_card.set(card)

    @property
    def ally(self):
        return self._ally.take()

    @ally.setter
    def ally(self, ally):
        self._ally.set(ally)

    @property
    def enemies(self):
        return self._enemies.take()

    @enemies.setter
    def enemies(self, enemies):
        self._enemies.set(enemies)

    # end SharedResources

    # CardModel SharedResources definitions

    @property
    def onboard_cards(self):
        return self._onboard_cards.take()

    @onboard_cards.setter
    def onboard_cards(self, enemies):
        self._onboard_cards.set(enemies)

    @property
    def previous_character(self):
        return self._previous_character.take()

    @previous_character.setter
    def previous_character(self, enemies):
        self._previous_character.set(enemies)

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(CardModel, self).__init__()

        self._onboard_cards = SharedResource()
        self._onboard_cards = list()

        self._previous_character = SharedResource()

    def _initialize(self):
        CardModel._initialized = True
        print("CardModel initialized")

        self._battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self._current_character = self._battle_logic._current_character
        self._current_card = self._battle_logic._current_card
        self._selected_card = self._battle_logic._selected_card
        self.selected_card_index = 0

        # Before first usage need to create copy and store as previous to initialize
        self.previous_character = self.current_character

    def on_create(self):
        self.position = self.property('TransformProperty').position
        self.position.y = 576
        self.position.x = 24

    # generuje BATTLEDECK dla danego CHARACTER
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

    # tasowanie talii
    @staticmethod
    def deck_shuffle(character):
        pass

    # dobieranie karty do HAND z DRAWPILE
    @staticmethod
    def draw_card(character):
        # dodać sprawdzanie czy można dobrać kartę z DRAWPILE
        card = character.draw_pile.pop(0)
        character.hand.append(card)
        character.hand[0].selected = True

    # dobieranie nowego HAND
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

            if signal.type == BattleLogic.SHUFFLE_DECK_SIGNAL and signal.subtype == "INITIAL":
                # print(f'Stare! CARD_MODEL:RECEIVED: "event": "SHUFFLE_DECK_SIGNAL", "subtype": "INITIAL"')
                Logs.DebugMessage.SignalReceived(self, signal)

                # print(f'Stare! CARD_MODEL:EMIT: "event": "SHUFFLE_DECK_RESPONSE", "subtype": "INITIAL"')
                signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_RESPONSE, {"event": "SHUFFLE_DECK_RESPONSE", "subtype": "INITIAL"})
                pygame.event.post(signal)
                Logs.DebugMessage.SignalEmit(self, signal)

                pass

        pass

    def _on_arrow_right(self, event):
        if event.key == pygame.K_RIGHT:

            if self.selected_card_index < len(self.current_character.hand) - 1:
                self.current_character.hand[self.selected_card_index].selected = False
                self.selected_card_index += 1
                print(f'{self.selected_card_index}')
                self.current_character.hand[self.selected_card_index].selected = True

                # Current Card to Info View

    def _on_arrow_left(self, event):
        if event.key == pygame.K_LEFT:
            if self.selected_card_index > 0:

                self.current_character.hand[self.selected_card_index].selected = False
                self.selected_card_index -= 1
                print(f'{self.selected_card_index}')
                self.current_character.hand[self.selected_card_index].selected = True

                # Current Card to Info View

    def _card_selection(self, event):
        if event.key == pygame.K_RETURN:

            self.current_card = self.current_character.hand[self.selected_card_index]
            self.current_card.current = True
            print(f'wybrana karta: {self._battle_logic.current_card.card_name}')

            BattleLogic.card_model_active = False

            # Call CURRENT_CARD_SIGNAL back to the BattleLogic
            signal = pygame.event.Event(BattleLogic.CURRENT_CARD_SIGNAL, {"event": "CURRENT_CARD_SIGNAL"})
            pygame.event.post(signal)
