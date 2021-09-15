import pygame

from property.initialize_property import InitializeState, InitializeProperty

from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource


class CharacterModel(GameObjectSharedResource):

    _initialized = False

    def __init__(self):
        super(CharacterModel, self).__init__()

        # For Arrow event
        self._target_confirmed = False
        self.selected_target_index = 0

    def _initialize(self):

        if InitializeProperty.check_status(self, InitializeState.INITIALIZED):
            super(CharacterModel, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "CharacterModel Initialized [ OK ]")

            return

        if InitializeProperty.check_status(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "CharacterModel Started [ OK ]")

            return

    # # dodaje bohaterów(CHARACTER) do puli sojuszników(ALLY)
    # def create_ally(self):
    #     for character in self._party_list:
    #         self.ally.append(character)
    #
    # # dodaje wrogów(ENEMY) do puli przeciwników(ENEMIES)
    # def create_enemies(self):
    #     for enemy in self._enemies_list:
    #         self.enemies.append(enemy)

    def on_script(self):
        pass

    def on_event(self, event):
            if event.type == pygame.KEYDOWN:
                self._on_arrow_right(event)
                self._on_arrow_left(event)
                self._card_selection(event)

    def on_signal(self, signal):

        # ChM1
        if signal.type == BattleLogic.CHARACTER_MODEL_SIGNAL and signal.subtype == "STANDARD" or \
                signal.type == BattleLogic.CHARACTER_MODEL_SIGNAL and signal.subtype == "TARGET_SELECTION":

            if signal.type == BattleLogic.CHARACTER_MODEL_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "ChM1<-BL12")
            if signal.type == BattleLogic.CHARACTER_MODEL_SIGNAL and signal.subtype == "TARGET_SELECTION":
                Logs.DebugMessage.SignalReceived(self, signal, "ChM1<-ChM1")

            # Arrows event block for target choose
            if signal.type == BattleLogic.CHARACTER_MODEL_SIGNAL and signal.subtype == "STANDARD":
                Logs.InfoMessage.SimpleInfo(self, "CHOOSE TARGET: ARROW EVENT LOOP STARTED")
                self._target_confirmed = False
                self.property('EventProperty').property_enable()
                emit_signal = pygame.event.Event(BattleLogic.CHARACTER_MODEL_SIGNAL, {"event": "CHARACTER_MODEL_SIGNAL", "subtype": "TARGET_SELECTION"})
                pygame.event.post(emit_signal)
                return

            if self._target_confirmed == False:
                Logs.InfoMessage.SimpleInfo(self, "PRESS ARROW")
                emit_signal = pygame.event.Event(BattleLogic.CHARACTER_MODEL_SIGNAL, {"event": "CHARACTER_MODEL_SIGNAL", "subtype": "TARGET_SELECTION"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "ChM1->ChM1")
                return

            if self._target_confirmed == True:
                Logs.InfoMessage.SimpleInfo(self, "TARGET SELECTED: ARROW EVENT LOOP FINISHED")
                self.property('EventProperty').property_disable()
                emit_signal = pygame.event.Event(BattleLogic.CHARACTER_MODEL_RESPONSE, {"event": "CHARACTER_MODEL_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "ChM1->BL13")
                return

    def _on_arrow_right(self, event):

        if event.key == pygame.K_RIGHT:
            Logs.DebugMessage.EventKeyPress(self, event, "K_RIGHT")
            if self.selected_target_index < len(self.battle_ally + self.battle_enemies) - 1:
                self.selected_target_index += 1
                self.selected_target = (self.battle_ally + self.battle_enemies)[self.selected_target_index]
                print(f'selected_target_index: {self.selected_target_index}, target: {self.selected_target.name}')

    def _on_arrow_left(self, event):

        if event.key == pygame.K_LEFT:
            Logs.DebugMessage.EventKeyPress(self, event, "K_LEFT")
            if self.selected_target_index > 0:
                self.selected_target_index -= 1
                self.selected_target = (self.battle_ally + self.battle_enemies)[self.selected_target_index]
                print(f'selected_target_index: {self.selected_target_index}, target: {self.selected_target.name}')

    def _card_selection(self, event):
        if event.key == pygame.K_RETURN:
            self._target_confirmed = True
            Logs.InfoMessage.SimpleInfo(self, "TARGET SELECTED")
            # TODO: It should be refactored to keep selected target object in variable not represent as a index in array
            self.confirmed_target = (self.battle_ally + self.battle_enemies)[self.selected_target_index]

            print(f'selected_target_index: {self.selected_target_index}')
            print(f'confirmed_target: {self._battle_logic.confirmed_target.name}')

            # BattleLogic.character_model_active = False
