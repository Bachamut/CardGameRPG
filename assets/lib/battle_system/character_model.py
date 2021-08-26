import pygame

from game_object.game_object import GameObject
from property.initialize_property import InitializeState, InitializeProperty

from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource


class CharacterModel(GameObjectSharedResource):

    _initialized = False

    def __init__(self):
        super(CharacterModel, self).__init__()

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

    # dodaje bohaterów(CHARACTER) do puli sojuszników(ALLY)
    def create_ally(self):
        for character in self._party_list:
            self.ally.append(character)

    # dodaje wrogów(ENEMY) do puli przeciwników(ENEMIES)
    def create_enemies(self):
        for enemy in self._enemies_list:
            self.enemies.append(enemy)

    def on_script(self):
        pass

    def on_event(self, event):
        if BattleLogic.character_model_active and CharacterModel._initialized:
            if event.type == pygame.KEYDOWN:
                self._on_arrow_right(event)
                self._on_arrow_left(event)
                self._card_selection(event)

    def on_signal(self, signal):

        # ChM1
        if signal.type == BattleLogic.CHARACTER_MODEL_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.SignalReceived(self, signal, "ChM1<-BL12")

            emit_signal = pygame.event.Event(BattleLogic.CHARACTER_MODEL_RESPONSE, {"event": "CHARACTER_MODEL_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "ChM1->BL13")
            return

    def _on_arrow_right(self, event):
        if event.key == pygame.K_RIGHT:
            if self.selected_target_index < len(self.enemies) - 1:
                self.selected_target_index += 1
                print(f'selected_target_index {self.selected_target_index}')

                BattleLogic.selected_target = self.enemies[self.selected_target_index]

    def _on_arrow_left(self, event):
        if event.key == pygame.K_LEFT:
            if self.selected_target_index > 0:
                self.selected_target_index -= 1
                print(f'selected_target_index {self.selected_target_index}')

                self.selected_target = self.enemies[self.selected_target_index]

    def _card_selection(self, event):
        if event.key == pygame.K_RETURN:

            # TODO: It should be refactored to keep selected target object in variable not represent as a index in array
            self.confirmed_target = self.enemies[self.selected_target_index]

            print(f'selected_target_index {self.selected_target_index}')
            print(f'confirmed_target {self._battle_logic.confirmed_target.name}')

            BattleLogic.character_model_active = False

            signal = pygame.event.Event(BattleLogic.TARGET_SELECTED_SIGNAL, {"event": "TARGET_SELECTED_SIGNAL"})
            pygame.event.post(signal)
