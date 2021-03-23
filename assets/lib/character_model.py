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
        self.queue_list = []

        self.character_list = {}

    def _initialize(self):
        CharacterModel._initialized = True

    def create_party(self):
        for character in self.party:
            self.party_list.append(character)

    def create_enemies(self):
        for enemy in self.enemies:
            self.enemy_list.append(enemy)

    # def update_queue(self):
    #     character_list = {}
    #     # self.queue_list = []
    #     units = self.party_list + self.enemy_list
    #     for unit in units:
    #         speed = unit.attributes.speed
    #         character_list[unit] = speed
    #     for value in range(0, len(character_list)):
    #         keymax = max(character_list, key=character_list.get)
    #         character_list.pop(keymax, None)
    #         self.queue_list.append(keymax)

    # def get_next(self):
    #     next_char = self.queue_list.pop(0)
    #     self.queue_list.append(next_char)
    #     queue = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
    #     print("\n")
    #     for character in queue.queue_list:
    #         print(character.name)
    #     print("\n")
    #     return next_char

    def create_queue(self):
        self.units = self.party_list + self.enemy_list
        for unit in self.units:
            speed = unit.attributes.speed
            self.character_list[unit] = speed

    def update_queue(self):
        while True:
            fastest_char = max(self.character_list, key=self.character_list.get)
            if self.character_list[fastest_char] >= 100:
                self.character_list[fastest_char] -= 100
                next_char = fastest_char
                print("\nEND LOOP")
                for character, speed in self.character_list.items():
                    print(f'{character.name} speed = {speed}')
                return next_char
                break
            else:
                for unit in self.units:
                    speed = unit.attributes.speed
                    self.character_list[unit] += speed
            print("\nIN LOOP")
            for character, speed in self.character_list.items():
                print(f'{character.name} speed = {speed}')

    def on_script(self):
        if not self._initialized and GameLogic._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        pass
