from assets.lib.battle_logic import BattleLogic, CHARACTER_CHANGED_SIGNAL
from assets.lib.game_logic import GameLogic
from assets.lib.queue_model import QueueModel
from game_object.game_object import GameObject


class CharacterModel(GameObject):

    _initialized = False
    active = BattleLogic.character_model_active

    def __init__(self):
        super(CharacterModel, self).__init__()
        self.character = BattleLogic.current_character
        self.target = BattleLogic.current_target

        self._party_list = GameLogic.party
        self._enemies_list = GameLogic.enemies

        self.party = []
        self.enemies = []


    def _initialize(self):
        CharacterModel._initialized = True

    def create_party(self):
        for character in self._party_list:
            self.party.append(character)

    def create_enemies(self):
        for enemy in self._enemies_list:
            self.enemies.append(enemy)

    def on_script(self):
        if not self._initialized and GameLogic._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass
