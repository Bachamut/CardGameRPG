from game_object.game_object import GameObject

from assets.lib.card_manager import CardManager
from assets.lib.character_manager import CharacterManager
from assets.lib.item_manager import ItemManager


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

        CardManager.load_config('assets/lib/card_types.json')
        CharacterManager.load_config('assets/lib/character_types.json')
        ItemManager.load_config('assets/lib/item_types.json')

        self._create_party()
        self._create_enemy()

    def _create_party(self):
        player = CharacterManager.create_character("character_edward")
        player.inventory.add_item('Short sword')
        player.inventory.add_item('Simple shield')
        player.add_equip('hand_r', 'Short sword')
        player.add_equip('hand_l', 'Simple shield')
        GameLogic.party.append(player)

        player = CharacterManager.create_character("character_lucius")
        player.deck['Nimble Strike'] = 4
        GameLogic.party.append(player)

    def _create_enemy(self):
        enemy = CharacterManager.create_character("warrior_goblin")
        enemy.deck['Fast Strike'] = 2
        enemy.deck['Piercing Strike'] = 1
        GameLogic.enemies.append(enemy)

        enemy = CharacterManager.create_character("archer_goblin")
        enemy.deck['Bow Shot'] = 3
        GameLogic.enemies.append(enemy)

    def on_create(self):
        pass

    def on_script(self):
        if not GameLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass



