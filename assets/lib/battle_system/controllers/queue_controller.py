import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.log import Logs
from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from resource_manager.shared_resource import SharedResource

from assets.lib.game_object_shared_resource import GameObjectSharedResource


class QueueController(GameObjectSharedResource):

    # QueueController SharedResources definitions

    @property
    def temporary_speeds(self):
        return self._temporary_speeds.take()

    @temporary_speeds.setter
    def temporary_speeds(self, enemies):
        self._temporary_speeds.set(enemies)

    @property
    def speeds_table(self):
        return self._speeds_table.take()

    @speeds_table.setter
    def speeds_table(self, enemies):
        self._speeds_table.set(enemies)

    @property
    def queue(self):
        return self._queue.take()

    @queue.setter
    def queue(self, enemies):
        self._queue.set(enemies)

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(QueueController, self).__init__()

        self._temporary_speeds = SharedResource()
        self._speeds_table = SharedResource()
        self._queue = SharedResource()

        self._speeds_table.set(dict())
        self._temporary_speeds.set(dict())
        self._queue.set(list())

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(QueueController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "QueueController Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "QueueController Started [ OK ]")

            return

    def setup_queue(self, units=None):
        if units is None:
            units = self.battle_ally + self.battle_enemies

        for character in units:
            self.speeds_table[character] = 0
            self.temporary_speeds[character] = 0

    def remove_character(self, character):
        self.speeds_table.pop(character)
        self.temporary_speeds.pop(character)

    @staticmethod
    def update_speed(speeds_table, characters_speed, temporary_speeds):
        for c in speeds_table:
            speeds_table[c] += characters_speed[c] + temporary_speeds[c]

    @staticmethod
    def get_next(speeds_table):
        fastest = max(speeds_table, key=speeds_table.get)
        if speeds_table[fastest] >= 100:
            return fastest
        elif speeds_table[fastest] < 100:
            return None

    @staticmethod
    def reduce_speed(speeds_table, character):
        speeds_table[character] -= 100

    def get_next_seed(self):
        return QueueController._get_next_seed(self.speeds_table, QueueController.get_speed_dict(self.battle_ally + self.battle_enemies), self.temporary_speeds)

    @staticmethod
    def _get_next_seed(speeds_table, character_speeds, temporary_speeds):

        simulation_table = speeds_table.copy()

        while True:
            character = QueueController.get_next(simulation_table)
            if character is not None:
                QueueController.reduce_speed(simulation_table, character)
                break
            elif character is None:
                QueueController.update_speed(simulation_table, character_speeds, temporary_speeds)

        return simulation_table

    def get_queue(self):
        return QueueController._get_queue(self.speeds_table, QueueController.get_speed_dict(self.battle_ally + self.battle_enemies), self.temporary_speeds)

    @staticmethod
    def get_speed_dict(characters):

        character_speeds = dict()

        for character in characters:
            character_speeds[character] = character.battle_attribute("speed")
        return character_speeds

    @staticmethod
    def _get_queue(speeds_table, character_speeds, temporary_speeds):

        simulation_table = speeds_table.copy()
        queue = list()

        quantity = 8
        while quantity - len(queue) != 0:
            character = QueueController.get_next(simulation_table)
            if character is not None:
                queue.append(character)
                QueueController.reduce_speed(simulation_table, character)
            elif character is None:
                QueueController.update_speed(simulation_table, character_speeds, temporary_speeds)

        return queue

    def on_script(self):
        pass

    def on_signal(self, signal):

        # QCS1
        if signal.type == BattleLogic.QUEUE_CONTROLLER_SIGNAL and signal.subtype == "INITIAL":
            Logs.DebugMessage.SignalReceived(self, signal, "QCS1<-BLS2")

            self.setup_queue()

            emit_signal = pygame.event.Event(BattleLogic.QUEUE_CONTROLLER_RESPONSE, {"event": "QUEUE_CONTROLLER_RESPONSE", "subtype": "INITIAL"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "QCS1->BLS3")
            return

        # QC1
        if signal.type == BattleLogic.QUEUE_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.SignalReceived(self, signal, "QC1<-BL1")

            # Taking next character from QueueController

            queue = self.get_queue()
            self.current_character = queue[0]

            next_seed = self.get_next_seed()

            # can be moved to get_next_seed()
            for key, values in self.speeds_table.items():
                self.speeds_table[key] = next_seed[key]

            self.queue = queue

            print(f'')
            for key, value in self.speeds_table.items():
                print(
                    f'{key.name}: {value} | {self.get_speed_dict(self.battle_ally + self.battle_enemies)[key]} +{self.temporary_speeds[key]}')
            print(f'CURRENT_CHARACTER: {self.current_character.name}')
            print(f'QUEUE:')
            for character in self.queue:
                print(f'- {character.name}')
            emit_signal = pygame.event.Event(BattleLogic.QUEUE_CONTROLLER_RESPONSE, {"event": "QUEUE_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "QC1->BL2")
            return
