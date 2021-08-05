import pygame

from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic


class CharacterModel(GameObject):

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

    _initialized = False

    def __init__(self):
        super(CharacterModel, self).__init__()

        self._battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self._current_character = self._battle_logic._current_character
        self._current_target = self._battle_logic._current_target
        self._selected_target = self._battle_logic._selected_target
        self._selected_target_index = 0

        self._ally = self._battle_logic._ally
        self._enemies = self._battle_logic._enemies

        _game_logic = GameObject.get_object_pool().select_with_label("GameLogic")[0]
        self._party_list = _game_logic.party
        self._enemies_list = _game_logic.enemies

    def _initialize(self):
        CharacterModel._initialized = True
        print("CharacterModel initialized")

    # dodaje bohaterów(CHARACTER) do puli sojuszników(ALLY)
    def create_ally(self):
        for character in self._party_list:
            self.ally.append(character)

    # dodaje wrogów(ENEMY) do puli przeciwników(ENEMIES)
    def create_enemies(self):
        for enemy in self._enemies_list:
            self.enemies.append(enemy)

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
        pass

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
            self.current_target = self.enemies[self.selected_target_index]

            print(f'selected_target_index {self.selected_target_index}')
            print(f'current_target {self._battle_logic.current_target.name}')

            BattleLogic.character_model_active = False

            signal = pygame.event.Event(BattleLogic.TARGET_SELECTED_SIGNAL, {"event": "TARGET_SELECTED_SIGNAL"})
            pygame.event.post(signal)
