from assets.lib.battle_logic import BattleLogic
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class CharacterModel(GameObject):

    _initialized = False
    active = BattleLogic.character_model_active

    def __init__(self):
        super(CharacterModel, self).__init__()
        self.current_character = BattleLogic.current_character
        self.current_target = BattleLogic.current_target

        self.ally = BattleLogic.ally
        self.enemies = BattleLogic.enemies

        self._party_list = GameLogic.party
        self._enemies_list = GameLogic.enemies

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
