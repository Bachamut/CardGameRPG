from assets.lib.battle_logic import BattleLogic
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class CharacterModel(GameObject):

    _initialized = False
    active = BattleLogic.character_model_active

    def __init__(self):
        super(CharacterModel, self).__init__()
        self.character = BattleLogic.current_character
        self.target = BattleLogic.current_target

        self.party = GameLogic.party
        self.enemies = GameLogic.enemies

        self.party_list = []
        self.enemy_list = []
        self.order_list = []

    def _initialize(self):
        CharacterModel._initialized = True

    def create_party(self):
        for character in self.party:
            self.party_list.append(character)

    def create_enemies(self):
        for enemy in self.enemies:
            self.enemy_list.append(enemy)

    def update_order(self):
        character_list = {}
        units = self.party_list + self.enemy_list
        for unit in units:
            speed = unit.attributes.speed
            character_list[unit] = speed
        for value in range(0, len(character_list)):
            keymax = max(character_list, key=character_list.get)
            character_list[keymax] = -1
            self.order_list.append(keymax)

    def get_next(self):
        next_char = self.order_list.pop(0)
        self.order_list.append(next_char)

        return next_char

    def on_script(self):
        if not self._initialized and GameLogic._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass
