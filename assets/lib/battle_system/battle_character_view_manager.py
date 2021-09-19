from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.game_logic import GameLogic


class BattleCharacterViewManager(GameObject):
    current_player = None
    players_list = []

    def __init__(self):
        super(CharacterView, self).__init__()
        self._initialized = False
        self.position = None

    def on_create(self):
        self.position = self.property('TransformProperty').position
        self.position.y = 300
        self.position.x = 200

    def _initialize(self):
        self._initialized = True
        print("CharacterView initialized")

        # TODO: These objects should be stored in CharacterModel (?)
        self.players = GameObject.get_object_pool().select_with_label('Players')[0]
        self.enemies = GameObject.get_object_pool().select_with_label('Enemies')[0]

        self.enemies.property('TransformProperty').position.x = 512
        self.attach_child(self.players)
        self.attach_child(self.enemies)
        self.position = self.property('TransformProperty').position
        self.position.x = 256
        self.position.y = 232

    def on_script(self):
        if not self._initialized and GameLogic._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass
