import pygame

from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic


class CharacterModel(GameObject):

    _initialized = False

    def __init__(self):
        super(CharacterModel, self).__init__()

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self.current_target = _battle_logic.current_target
        self.selected_target = _battle_logic.selected_target
        self.selected_target_index = 0

        self.ally = _battle_logic.ally
        self.enemies = _battle_logic.enemies

        _game_logic = GameObject.get_object_pool().select_with_label("GameLogic")[0]
        self._party_list = _game_logic.party
        self._enemies_list = _game_logic.enemies

    def _initialize(self):
        CharacterModel._initialized = True
        print("CharacterModel initialized")

    def create_ally(self):
        for character in self._party_list:
            self.ally.take().append(character)

    def create_enemies(self):
        for enemy in self._enemies_list:
            self.enemies.take().append(enemy)

    def on_script(self):
        if not self._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        if BattleLogic.character_model_active and CharacterModel._initialized:
            if event.type == pygame.KEYDOWN:
                self._on_arrow_right(event)
                self._on_arrow_left(event)
                self._card_selection(event)

    def on_signal(self, signal):
        if signal.type == BattleLogic.CHARACTER_ACTIVE_SIGNAL:
            BattleLogic.character_model_active = True
            self.selected_target_index = 0

    def _on_arrow_right(self, event):
        if event.key == pygame.K_RIGHT:
            if self.selected_target_index < len(self.enemies.take()) - 1:
                self.selected_target_index += 1
                print(f'selected_target_index {self.selected_target_index}')

                self.selected_target.update(GameObject.get_object_pool().select_with_label("BattleLogic")[0].selected_target)
                self.enemies = GameObject.get_object_pool().select_with_label("BattleLogic")[0].enemies
                BattleLogic.selected_target.update(self.enemies.take()[self.selected_target_index])

    def _on_arrow_left(self, event):
        if event.key == pygame.K_LEFT:
            if self.selected_target_index > 0:
                self.selected_target_index -= 1
                print(f'selected_target_index {self.selected_target_index}')

                self.selected_target.update(GameObject.get_object_pool().select_with_label("BattleLogic")[0].selected_target)
                self.enemies = GameObject.get_object_pool().select_with_label("BattleLogic")[0].enemies
                BattleLogic.selected_target.update(self.enemies.take()[self.selected_target_index])

    def _card_selection(self, event):
        if event.key == pygame.K_RETURN:

            _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

            BattleLogic.current_target.update(self.enemies.take()[self.selected_target_index])

            print(f'selected_target_index {self.selected_target_index}')
            print(f'current_target {BattleLogic.current_target.take().name}')

            BattleLogic.character_model_active = False

            signal = pygame.event.Event(BattleLogic.TARGET_SELECTED_SIGNAL, {"event": "TARGET_SELECTED_SIGNAL"})
            pygame.event.post(signal)
