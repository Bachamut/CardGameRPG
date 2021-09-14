import random

import pygame

from random import sample
from game_object.game_object import GameObject
from property.initialize_property import InitializeState, InitializeProperty

from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.game_logic import GameLogic
from resource_manager.shared_resource import SharedResource
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource

CARD_VIEW_ON_RISE = pygame.event.custom_type()
CARD_VIEW_ON_FALL = pygame.event.custom_type()


class CardModel(GameObjectSharedResource):


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

        if InitializeProperty.check_status(self, InitializeState.INITIALIZED):
            super(CardModel, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "CardModel Initialized [ OK ]")

            return

        if InitializeProperty.check_status(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "CharacterModel Started [ OK ]")

            return

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
                character.battle_deck.append(card_instance)
        # creating draw_pile that is used in battle mode
        character.draw_pile = sample(character.battle_deck, len(character.battle_deck))

    # tasowanie talii
    @staticmethod
    def shuffle_deck(character):
        for it in range(0, len(character.discard_pile)):
            CardModel.revert_discard(character)
        random.shuffle(character.draw_pile)

    @staticmethod
    def revert_discard(character):
        moved_card = character.discard_pile.pop(0)
        character.draw_pile.append(moved_card)

    @staticmethod
    def discard_draw_pile(character):
        for it in range(0, len(character.draw_pile)):
            CardModel.discard_top_card(character)

    @staticmethod
    def discard_top_card(character):
        discarded_card = character.draw_pile.pop(0)
        character.discard_pile.append(discarded_card)

    # dobieranie karty do HAND z DRAWPILE
    @staticmethod
    def draw_card(character):
        card = character.draw_pile.pop(0)
        character.hand.append(card)
        character.hand[0].selected = True

    # dobieranie nowego HAND
    @staticmethod
    def draw_hand(character):
        for it in range(0, character.card_draw):
            CardModel.draw_card(character)

    @staticmethod
    def discard_hand_card(character):
        card = character.hand.pop(0)
        character.discard_pile.append(card)

    @staticmethod
    def discard_hand(character):
        for it in range(0, len(character.hand)):
            CardModel.discard_hand_card(character)

    def on_script(self):
        pass

    def on_event(self, event):
        if BattleLogic.card_model_active and CardModel._initialized:

            if event.type == pygame.KEYDOWN:
                self._on_arrow_right(event)
                self._on_arrow_left(event)
                self._card_selection(event)
        pass

    def on_signal(self, signal):

            # CMS1
            if signal.type == BattleLogic.SHUFFLE_DECK_SIGNAL and signal.subtype == "INITIAL":
                Logs.DebugMessage.SignalReceived(self, signal, "CMS1<-BLS2")

                # Shuffling deck
                for character in (self.battle_ally + self.battle_enemies):
                    CardModel.shuffle_deck(character)

                emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_RESPONSE, {"event": "SHUFFLE_DECK_RESPONSE", "subtype": "INITIAL"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "CMS1->BL1")
                return

            # CM2
            if signal.type == BattleLogic.SHUFFLE_DECK_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "CM2<-BL3A")

                # Deck shuffle if there is no cards in draw_pile
                CardModel.shuffle_deck(self.current_character)

                emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_RESPONSE, {"event": "SHUFFLE_DECK_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "CM2->BL4")
                return

            # CM3
            if signal.type == BattleLogic.DRAW_CARD_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "CM3<-BL5")

                # Draw_hand
                CardModel.draw_card(self.current_character)
                print(f'{self.current_character.name} hand: {self.current_character.hand}')

                emit_signal = pygame.event.Event(BattleLogic.DRAW_CARD_RESPONSE, {"event": "DRAW_CARD_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "CM3->BL6")
                return

            # CM4
            if signal.type == BattleLogic.CARD_MODEL_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "CM4<-BL10")

                emit_signal = pygame.event.Event(BattleLogic.CARD_MODEL_RESPONSE, {"event": "CARD_MODEL_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "CM4->BL12")
                return


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

            self.confirmed_card = self.current_character.hand[self.selected_card_index]
            self.confirmed_card.current = True
            print(f'wybrana karta: {self._battle_logic.confirmed_card.card_name}')

            BattleLogic.card_model_active = False

            # Call confirmed_card_SIGNAL back to the BattleLogic
            signal = pygame.event.Event(BattleLogic.confirmed_card_SIGNAL, {"event": "confirmed_card_SIGNAL"})
            pygame.event.post(signal)
