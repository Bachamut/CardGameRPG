import pygame

from assets.lib.battle_system.log import Logs
from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from resource_manager.shared_resource import SharedResource


class QueueModel(GameObject):

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

    # QueueModel SharedResources definitions

    @property
    def characters_speed(self):
        return self._characters_speed.take()

    @characters_speed.setter
    def characters_speed(self, enemies):
        self._characters_speed.set(enemies)

    @property
    def modifiers(self):
        return self._modifiers.take()

    @modifiers.setter
    def modifiers(self, enemies):
        self._modifiers.set(enemies)

    @property
    def party(self):
        return self._party.take()

    @party.setter
    def party(self, enemies):
        self._party.set(enemies)

    @property
    def queue(self):
        return self._queue.take()

    @queue.setter
    def queue(self, enemies):
        self._queue.set(enemies)

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(QueueModel, self).__init__()

        self._characters_speed = SharedResource()
        self._modifiers = SharedResource()
        self._party = SharedResource()
        self._queue = SharedResource()

        self._characters_speed.set(dict())
        self._modifiers.set(dict())
        self._party.set(dict())
        self._queue.set(list())

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self._current_character = _battle_logic._current_character
        self._ally = _battle_logic._ally
        self._enemies = _battle_logic._enemies

        _game_logic = GameObject.get_object_pool().select_with_label("GameLogic")[0]
        self._party_list = _game_logic.party
        self._enemies_list = _game_logic.enemies

    def _initialize(self):
        QueueModel._initialized = True
        print("QueueModel initialized")

    def setup_queue(self, units=None):
        if units is None:
            units = self.ally + self.enemies

        for character in units:
            self.add_character(character)

    def add_character(self, character):
        self.characters_speed[character] = character.attributes.speed
        self.party[character] = 0
        self.modifiers[character] = 0

    def remove_character(self, character):
        self.characters_speed.pop(character)
        self.party.pop(character)
        self.modifiers.pop(character)

    @staticmethod
    def update_speed(party, characters_speed, modifiers):
        for c in party:
            party[c] += characters_speed[c] + modifiers[c]

    @staticmethod
    def get_next(party):
        fastest = max(party, key=party.get)
        if party[fastest] >= 100:
            return fastest
        elif party[fastest] < 100:
            return None

    @staticmethod
    def reduce_speed(party, character):
        party[character] -= 100

    def get_next_seed(self):
        return QueueModel._get_next_seed(self.party, self.characters_speed, self.modifiers )

    @staticmethod
    def _get_next_seed(party, character_speeds, modifiers):
        party_seed = dict()

        for key, value in party.items():
            party_seed[key] = value

        while True:
            character = QueueModel.get_next(party_seed)
            if character is not None:
                QueueModel.reduce_speed(party_seed, character)
                break
            elif character is None:
                QueueModel.update_speed(party_seed, character_speeds, modifiers)

        return party_seed

    def get_queue(self):
        return QueueModel._get_queue(self.party, self.characters_speed, self.modifiers)

    @staticmethod
    def _get_queue(party, character_speeds, modifiers):
        party_seed = dict()
        queue = list()

        for key, value in party.items():
            party_seed[key] = value

        quantity = 8
        while quantity - len(queue) != 0:
            character = QueueModel.get_next(party_seed)
            if character is not None:
                queue.append(character)
                QueueModel.reduce_speed(party_seed, character)
            elif character is None:
                QueueModel.update_speed(party_seed, character_speeds, modifiers)

        return queue

    def on_script(self):
        if not QueueModel._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass

    def on_signal(self, signal):
        if QueueModel._initialized:

            # QM1
            if signal.type == BattleLogic.QUEUE_MODEL_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "QM1<-BL1")

                emit_signal = pygame.event.Event(BattleLogic.QUEUE_MODEL_RESPONSE, {"event": "QUEUE_MODEL_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "QM1->BL2")
                return