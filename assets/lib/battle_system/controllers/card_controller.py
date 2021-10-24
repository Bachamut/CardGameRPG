import random

import pygame

from random import sample
from game_object.game_object import GameObject
from property.initialize_property import InitializeState, InitializeProperty

from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.card_utilities.card_manager import CardManager
from resource_manager.shared_resource import SharedResource
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource

CARD_VIEW_ON_RISE = pygame.event.custom_type()
CARD_VIEW_ON_FALL = pygame.event.custom_type()


class CardController(GameObjectSharedResource):


    # CardController SharedResources definitions

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
        super(CardController, self).__init__()

        self._onboard_cards = SharedResource()
        self._onboard_cards = list()

        self._previous_character = SharedResource()
        # self._previous_character = self.current_character

        # For Arrow event
        self._card_confirmed = False
        self.selected_card_index = 0


    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(CardController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "CardController Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "CharacterController Started [ OK ]")

            return

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

    @staticmethod
    def shuffle_deck(character):
        for it in range(0, len(character.discard_pile)):
            CardController.revert_discard(character)
        random.shuffle(character.draw_pile)

    @staticmethod
    def revert_discard(character):
        moved_card = character.discard_pile.pop(0)
        character.draw_pile.append(moved_card)

    @staticmethod
    def discard_draw_pile(character):
        for it in range(0, len(character.draw_pile)):
            CardController.discard_top_card(character)

    @staticmethod
    def discard_top_card(character):
        discarded_card = character.draw_pile.pop(0)
        character.discard_pile.append(discarded_card)

    @staticmethod
    def draw_card(character):
        card = character.draw_pile.pop(0)
        character.hand.append(card)
        character.hand[0].selected = True
        Logs.CardControllerMessage.draw_card_info(card, character)

    @staticmethod
    def draw_hand(character):
        for it in range(0, character.card_draw):
            CardController.draw_card(character)

    @staticmethod
    def discard_hand_card(character):
        card = character.hand.pop(0)
        character.discard_pile.append(card)

    @staticmethod
    def discard_used_card(character, card):
        character.hand.remove(card)
        character.discard_pile.append(card)

    @staticmethod
    def discard_hand(character):
        for it in range(0, len(character.hand)):
            CardController.discard_hand_card(character)

    def on_script(self):
        pass

    def on_event(self, event):

        if event.type == pygame.KEYDOWN:
            self._on_arrow_right(event)
            self._on_arrow_left(event)
            self._card_selection(event)
        pass

    def on_signal(self, signal):

            # CCS1
            if signal.type == BattleLogic.SHUFFLE_DECK_SIGNAL and signal.subtype == "INITIAL":
                Logs.DebugMessage.signal_received(self, signal, "CCS1<-BLS3")

                # Shuffling deck
                for character in (self.battle_ally + self.battle_enemies):
                    CardController.shuffle_deck(character)

                emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_RESPONSE, {"event": "SHUFFLE_DECK_RESPONSE", "subtype": "INITIAL"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "CCS1->BLS4")
                return

            # CC2
            if signal.type == BattleLogic.SHUFFLE_DECK_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.signal_received(self, signal, "CC2<-BL3A")

                # Deck shuffle if there is no cards in draw_pile
                CardController.shuffle_deck(self.current_character)

                emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_RESPONSE, {"event": "SHUFFLE_DECK_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "CC2->BL4")
                return

            # CC3
            if signal.type == BattleLogic.DRAW_CARD_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.signal_received(self, signal, "CC3<-BL5")

                # Card_draw
                CardController.draw_card(self.current_character)
                # print(f'{self.current_character.name} hand: {self.current_character.hand}')

                emit_signal = pygame.event.Event(BattleLogic.DRAW_CARD_RESPONSE, {"event": "DRAW_CARD_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "CC3->BL6")
                return

            # CC4
            if signal.type == BattleLogic.CARD_CONTROLLER_SIGNAL and signal.subtype == "STANDARD" or \
                    signal.type == BattleLogic.CARD_CONTROLLER_SIGNAL and signal.subtype == "CARD_SELECTION":

                if signal.type == BattleLogic.CARD_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "CC4<-BL9")
                # if signal.type == BattleLogic.CARD_CONTROLLER_SIGNAL and signal.subtype == "CARD_SELECTION":
                #     Logs.DebugMessage.SignalReceived(self, signal, "CC4<-CC4")

                # Arrows event block for card choose
                if signal.type == BattleLogic.CARD_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
                    Logs.InfoMessage.simple_info(self, "ARROW EVENT LOOP STARTED")
                    self._card_confirmed = False

                    # Set first card from hand as Selected.
                    # (Used by CardViewController to display arrow on first Card on hand before and arrow event)
                    self.selected_card = self.current_character.hand[0]

                    self.property('EventProperty').property_enable()
                    emit_signal = pygame.event.Event(BattleLogic.CARD_CONTROLLER_SIGNAL, {"event": "CARD_CONTROLLER_SIGNAL", "subtype": "CARD_SELECTION"})
                    pygame.event.post(emit_signal)
                    return

                if self._card_confirmed == False:
                    # Logs.InfoMessage.SimpleInfo(self, "PRESS ARROW")
                    emit_signal = pygame.event.Event(BattleLogic.CARD_CONTROLLER_SIGNAL, {"event": "CARD_CONTROLLER_SIGNAL", "subtype": "CARD_SELECTION"})
                    pygame.event.post(emit_signal)
                    # Logs.DebugMessage.SignalEmit(self, emit_signal, "CC4->CC4")
                    return

                if self._card_confirmed == True:
                    Logs.InfoMessage.simple_info(self, "ARROW EVENT LOOP FINISHED")
                    self.property('EventProperty').property_disable()
                    # Set previous_character
                    self.previous_character = self.current_character
                    emit_signal = pygame.event.Event(BattleLogic.CARD_CONTROLLER_RESPONSE, {"event": "CARD_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "CC4->BL12")
                    return

    def _on_arrow_right(self, event):

        if event.key == pygame.K_RIGHT:
            Logs.DebugMessage.event_key_press(self, event, "K_RIGHT")
            if self.selected_card_index < len(self.current_character.hand) - 1:
                self.current_character.hand[self.selected_card_index].selected = False
                self.selected_card_index += 1
                print(f'{self.selected_card_index}: {self.current_character.hand[self.selected_card_index].card_name}')
                self.current_character.hand[self.selected_card_index].selected = True

                # Mark Card as Selected
                self.selected_card = self.current_character.hand[self.selected_card_index]

    def _on_arrow_left(self, event):

        if event.key == pygame.K_LEFT:
            Logs.DebugMessage.event_key_press(self, event, "K_LEFT")
            if self.selected_card_index > 0:
                self.current_character.hand[self.selected_card_index].selected = False
                self.selected_card_index -= 1
                print(f'{self.selected_card_index}: {self.current_character.hand[self.selected_card_index].card_name}')
                self.current_character.hand[self.selected_card_index].selected = True

                # Mark Card as Selected
                self.selected_card = self.current_character.hand[self.selected_card_index]

    def _card_selection(self, event):

        if event.key == pygame.K_RETURN:
            selected_card = CardManager.create_battle_card(self.current_character.hand[self.selected_card_index])
            if selected_card.ap_cost <= self.current_character.battle_attribute("action_points"):
                self._card_confirmed = True
                Logs.InfoMessage.simple_info(self, "CARD SELECTED")

                self.confirmed_card = self.current_character.hand[self.selected_card_index]
                self.confirmed_card.current = True
                print(f'wybrana karta: {self.selected_card_index}: {self._battle_logic.confirmed_card.card_name}')
            else:
                print(f'Nie masz wystarczającej ilość AP')

