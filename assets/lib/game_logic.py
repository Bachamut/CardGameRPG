from game_object.game_object import GameObject

from assets.lib.battle_system.ai_utilities.ai_condition_manager import AIConditionManager
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.character_utilities.character_manager import CharacterManager
from assets.lib.item_utilities.item_manager import ItemManager
from assets.lib.status_utilities.status_manager import StatusManager


class GameLogic(GameObject):

    party = []
    enemies = []
    _initialized = False

    def __init__(self):
        super(GameLogic, self).__init__()
        self.character_container = None
        self.card_container = None

    def _initialize(self):
        GameLogic._initialized = True

        CardManager.load_config('assets/lib/templates/card_types.json')
        CharacterManager.load_config('assets/lib/templates/character_types.json')
        ItemManager.load_config('assets/lib/templates/item_types.json')
        StatusManager.load_config('assets/lib/templates/status_types.json')
        AIConditionManager.load_config('assets/lib/templates/condition_blocks.json')

        self._create_party()
        self._create_enemy()
        # self._create_status_types()

    def _create_party(self):
        player = CharacterManager.create_character("character_edward")
        player.inventory.add_item('Short sword')
        player.inventory.add_item('Simple shield')
        player.add_equip('hand_r', 'Short sword')
        player.add_equip('hand_l', 'Simple shield')
        GameLogic.party.append(player)

        player = CharacterManager.create_character("character_lucius")
        player.inventory.add_item('Short sword')
        player.add_equip('hand_r', 'Short sword')
        GameLogic.party.append(player)

    def _create_enemy(self):
        enemy = CharacterManager.create_character("warrior_goblin")
        enemy.inventory.add_item('Short sword')
        enemy.add_equip('hand_r', 'Short sword')
        GameLogic.enemies.append(enemy)

    # def _create_status_types(self):
    #     StatusManager.create_status_types()
    #     print(f'status_types:')
    #     for status_type in StatusManager.status_type_list:
    #         print(f'{status_type.status_id}')
        
    def on_create(self):
        pass

    def on_script(self):
        if not GameLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass



