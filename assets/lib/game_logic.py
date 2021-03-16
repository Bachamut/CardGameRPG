from game_object.game_object import GameObject

from assets.lib.card_manager import CardManager
from assets.lib.character_manager import CharacterManager
from assets.lib.item_manager import ItemManager


class GameLogic(GameObject):

    # current_player = None
    # players_list = []
    initialized = False

    def __init__(self):
        super(GameLogic, self).__init__()
        self.character_container = None
        self.card_container = None

    def _initialize(self):
        GameLogic.initialized = True

        CardManager.load_config('assets/lib/card_types.json')
        CharacterManager.load_config('assets/lib/character_types.json')
        ItemManager.load_config('assets/lib/item_types.json')

        self.character_container = GameObject.get_object_pool().select_with_label('CharacterContainer')[0]
        self.card_container = GameObject.get_object_pool().select_with_label('CardContainer')[0]
        self.character_container.on_create()
        self.card_container.on_create()

        # player = CharacterManager.create_character("character_edward")
        # goblin = CharacterManager.create_character("character_goblin")
        # GameLogic.players_list.append(player)
        # GameLogic.players_list.append(goblin)
        # GameLogic.current_player = GameLogic.players_list[0]
        #
        # GameLogic.current_player.inventory.add_item('Short sword')
        # GameLogic.current_player.add_equip('hand_r', 'Short sword')

    def on_create(self):
        pass

    def on_script(self):
        if not GameLogic.initialized and len(GameObject.get_object_pool().select_with_label('CardContainer')) != 0:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass



