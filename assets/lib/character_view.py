from assets.lib.character_manager import CharacterManager
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class CharacterView(GameObject):
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

        # player = CharacterManager.create_character("character_edward")
        # goblin = CharacterManager.create_character("character_goblin")
        # CharacterView.players_list.append(player)
        # CharacterView.players_list.append(goblin)
        # CharacterView.current_player = CharacterView.players_list[0]
        #
        # CharacterView.current_player.inventory.add_item('Short sword')
        # CharacterView.current_player.inventory.add_item('Simple shield')
        # CharacterView.current_player.add_equip('hand_r', 'Short sword')
        # CharacterView.current_player.add_equip('hand_l', 'Simple shield')


    def on_script(self):
        if not self._initialized and GameLogic._initialized:
            self._initialize()
        else:
            pass