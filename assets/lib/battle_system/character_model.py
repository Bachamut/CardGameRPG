from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.game_logic import GameLogic


class CharacterModel(GameObject):

    _initialized = False
    active = BattleLogic.character_model_active

    def __init__(self):
        super(CharacterModel, self).__init__()

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self.current_character = _battle_logic.current_character
        # self.current_character = BattleLogic.current_character
        self.current_target = _battle_logic.current_target
        self.ally = _battle_logic.ally
        self.enemies = _battle_logic.enemies

        _game_logic = GameObject.get_object_pool().select_with_label("GameLogic")[0]
        self._party_list = _game_logic.party
        self._enemies_list = _game_logic.enemies

    def _initialize(self):
        CharacterModel._initialized = True

    def create_ally(self):
        for character in self._party_list:
            self.ally.append(character)

    def create_enemies(self):
        for enemy in self._enemies_list:
            self.enemies.append(enemy)

    def on_script(self):
        if not self._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass
