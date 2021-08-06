import pygame

from game_object.game_object import GameObject
from assets.lib.game_logic import GameLogic
from resource_manager.shared_resource import SharedResource
from assets.lib.battle_system.log import Logs


class BattleLogic(GameObject):

    BATTLE_LOGIC_SIGNAL = pygame.event.custom_type()

    SHUFFLE_DECK_SIGNAL = pygame.event.custom_type()
    QUEUE_MODEL_SIGNAL = pygame.event.custom_type()
    ACTION_MODEL_SIGNAL = pygame.event.custom_type()
    SHUFFLE_DECK_SIGNAL = pygame.event.custom_type()
    DRAW_CARD_SIGNAL = pygame.event.custom_type()
    CARD_MODEL_SIGNAL = pygame.event.custom_type()
    ITEM_MODEL_SIGNAL = pygame.event.custom_type()
    CHARACTER_MODEL_SIGNAL = pygame.event.custom_type()

    SHUFFLE_DECK_RESPONSE = pygame.event.custom_type()
    QUEUE_MODEL_RESPONSE = pygame.event.custom_type()
    ACTION_MODEL_RESPONSE = pygame.event.custom_type()
    SHUFFLE_DECK_RESPONSE = pygame.event.custom_type()
    DRAW_CARD_RESPONSE = pygame.event.custom_type()
    CARD_MODEL_RESPONSE = pygame.event.custom_type()
    ITEM_MODEL_RESPONSE = pygame.event.custom_type()
    CHARACTER_MODEL_RESPONSE = pygame.event.custom_type()

    character_model_active = False
    card_model_active = False
    turn_model_active = False

    _initialized = False
    started = False

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


    def __init__(self):
        super(BattleLogic, self).__init__()

        self.queue_model = None

        ###
        self._current_character = SharedResource()
        self._current_target = SharedResource()
        self._selected_target = SharedResource()
        self._current_card = SharedResource()
        self._selected_card = SharedResource()

        self._ally = SharedResource()
        self._ally.set(list())

        self._enemies = SharedResource()
        self._enemies.set(list())

        ###

    def _initialize(self):
        BattleLogic._initialized = True
        print("BattleLogic initialized")

    def on_script(self):
        if not self._initialized and GameLogic._initialized:
            self._initialize()
        else:
            pass

        if BattleLogic.started == False \
            and len(GameObject.get_object_pool().select_with_label('CharacterModel')) != 0 \
            and len(GameObject.get_object_pool().select_with_label('CardModel')) != 0 \
            and len(GameObject.get_object_pool().select_with_label('QueueModel')) != 0 \
            and len(GameObject.get_object_pool().select_with_label('CardView')) != 0:

            BattleLogic.started = True

            print(f'BATTLE_LOGIC:EMIT_SIGNAL: "event": "BATTLE_LOGIC_SIGNAL", "subtype": "INITIAL"')
            signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "INITIAL"})
            pygame.event.post(signal)


        elif BattleLogic.started == True:
            # signal = pygame.event.Event(CHARACTER_CHANGED)
            # pygame.event.post(signal)
            pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pass

    def on_signal(self, signal):
        if BattleLogic._initialized:

            # BATTLE_LOGIC INITIAL
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "INITIAL":
                # LogMessage DebugMessage InfoMessage
                # print(f'Stare! BATTLE_LOGIC:RECEIVED: "event": "BATTLE_LOGIC_SIGNAL", "subtype": "INITIAL"')
                Logs.DebugMessage.SignalReceived(self, signal)

                # print(f'Stare! BATTLE_LOGIC:EMIT: "event": "SHUFFLE_DECK_SIGNAL", "subtype": "INITIAL"')
                signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_SIGNAL, {"event": "SHUFFLE_DECK_SIGNAL", "subtype": "INITIAL"})
                pygame.event.post(signal)
                Logs.DebugMessage.SignalEmit(self, signal)
                pass

            # BATTLE_LOGIC FLOW

            if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "INITIAL":

                # print(f'Stare! BATTLE_LOGIC:RECEIVED "event": "SHUFFLE_DECK_RESPONSE", "subtype": "INITIAL"')
                Logs.DebugMessage.SignalReceived(self, signal)

                # print(f'Stare! BATTLE_LOGIC:EMIT: "event": "QUEUE_MODEL_SIGNAL", "subtype": "STANDARD"')
                signal = pygame.event.Event(BattleLogic.QUEUE_MODEL_SIGNAL, {"event": "QUEUE_MODEL_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(signal)
                Logs.DebugMessage.SignalEmit(self, signal)
                pass

            if signal.type == BattleLogic.QUEUE_MODEL_RESPONSE and signal.subtype == "STANDARD":

                Logs.DebugMessage.SignalReceived(self, signal)

                signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "PRE_TURN"})
                pygame.event.post(signal)
                Logs.DebugMessage.SignalEmit(self, signal)
                pass

            if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "PRE_TURN":

                Logs.DebugMessage.SignalReceived(self, signal)

                signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "PRE_DRAW"})
                pygame.event.post(signal)
                Logs.DebugMessage.SignalEmit(self, signal)
                pass


            pass
