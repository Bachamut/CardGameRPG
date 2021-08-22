from game_object.game_object import GameObject
from resource_manager.shared_resource import SharedResource


class GameObjectBattleShared(GameObject):

    def __init__(self):
        super(GameObjectBattleShared, self).__init__()

        self._current_character = SharedResource()
        self._current_target = SharedResource()
        self._selected_target = SharedResource()
        self._current_card = SharedResource()
        self._selected_card = SharedResource()

        self._battle_ally = SharedResource()
        self._battle_ally.set(list())

        self._battle_enemies = SharedResource()
        self._battle_enemies.set(list())

        self._base_ally = SharedResource()
        self._base_enemies = SharedResource()

    def _initialize(self):

        self._battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self._current_character = self._battle_logic._current_character
        self._current_target = self._battle_logic._current_target
        self._selected_target = self._battle_logic._selected_target
        self._current_card = self._battle_logic._current_card
        self._selected_card = self._battle_logic._selected_card

        self._battle_ally = self._battle_logic._battle_ally
        self._battle_enemies = self._battle_logic._battle_enemies

        _game_logic = GameObject.get_object_pool().select_with_label("GameLogic")[0]
        self._base_ally = _game_logic.party
        self._base_enemies = _game_logic.enemies


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
    def battle_ally(self):
        return self._battle_ally.take()

    @battle_ally.setter
    def ally(self, ally):
        self._battle_ally.set(ally)

    @property
    def battle_enemies(self):
        return self._battle_enemies.take()

    @battle_enemies.setter
    def battle_enemies(self, enemies):
        self._battle_enemies.set(enemies)

    # end SharedResources