from assets.lib.battle_logic import BattleLogic, CHARACTER_CHANGED
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
        self.queue_model = None

        self.party = GameLogic.party
        self.enemies = GameLogic.enemies

        self.party_list = []
        self.enemy_list = []
        self.queue_list = []

        self.character_list = {}

    def _initialize(self):
        CharacterModel._initialized = True
        self.queue_model = QueueModel(self)

    def create_party(self):
        for character in self.party:
            self.party_list.append(character)

    def create_enemies(self):
        for enemy in self.enemies:
            self.enemy_list.append(enemy)

    def on_script(self):
        if not self._initialized and GameLogic._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass
