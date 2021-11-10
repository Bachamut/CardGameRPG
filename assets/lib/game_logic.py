import json

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

        card_config, character_config, item_config, status_config, ai_config = GameLogic._load_config_preset('game_logic_test')

        CardManager.load_config(card_config)
        CharacterManager.load_config(character_config)
        ItemManager.load_config(item_config)
        StatusManager.load_config(status_config)
        AIConditionManager.load_config(ai_config)

        self._create_party()
        self._create_enemy()

    @staticmethod
    def _load_config_preset(setup_name):

        filename = 'assets/lib/templates/game_logic_config.json'

        with open(filename, 'r') as file:
            config = json.load(file)
            for key, value in config.items():
                CardManager.card_config.update({key: value})

        config_paths = config[setup_name]

        card_config = config_paths['card_config']
        character_config = config_paths['character_config']
        item_config = config_paths['item_config']
        status_config = config_paths['status_config']
        ai_config = config_paths['ai_config']

        return card_config, character_config, item_config, status_config, ai_config

    def _create_party(self):
        player = CharacterManager.create_character("character_edward")
        player.state = "alive"
        player.inventory.add_item('Short sword')
        player.inventory.add_item('Simple shield')
        player.add_equip('hand_r', 'Short sword')
        player.add_equip('hand_l', 'Simple shield')
        player.deck['multi_strike_1'] = 2
        player.deck['counter_stance_1'] = 1
        GameLogic.party.append(player)

        # player = CharacterManager.create_character("character_lucius")
        # player.state = "alive"
        # player.inventory.add_item('Short sword')
        # player.add_equip('hand_r', 'Short sword')
        # GameLogic.party.append(player)

    def _create_enemy(self):
        enemy = CharacterManager.create_character("warrior_goblin")
        enemy.state = "alive"
        enemy.inventory.add_item('Short sword')
        enemy.add_equip('hand_r', 'Short sword')
        # enemy.deck['multi_strike_1'] = 5
        enemy.deck['counter_stance_1'] = 1
        # enemy.deck['fast_strike_1'] = 5
        GameLogic.enemies.append(enemy)

        # enemy = CharacterManager.create_character("healer_goblin")
        # enemy.state = "alive"
        # enemy.inventory.add_item('Healer wand')
        # enemy.add_equip('hand_r', 'Healer wand')
        # GameLogic.enemies.append(enemy)

    def on_create(self):
        pass

    def on_script(self):
        if not GameLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass



