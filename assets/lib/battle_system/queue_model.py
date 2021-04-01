from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic


class QueueModel(GameObject):

    _initialized = False

    def __init__(self):
        super(QueueModel, self).__init__()

        self.characters_speed = dict()
        self.modifiers = dict()
        self.party = dict()
        self.queue = list()

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self.current_character = _battle_logic.current_character
        self.ally = _battle_logic.ally
        self.enemies = _battle_logic.enemies

        _game_logic = GameObject.get_object_pool().select_with_label("GameLogic")[0]
        self._party_list = _game_logic.party
        self._enemies_list = _game_logic.enemies

    def _initialize(self):
        QueueModel._initialized = True
        print("QueueModel initialized")

    def setup_queue(self, units=None):
        if units is None:
            units = self.ally + self.enemies

        for character in units:
            self.add_character(character)

    def add_character(self, character):
        self.characters_speed[character] = character.attributes.speed
        self.party[character] = 0
        self.modifiers[character] = 0

    def remove_character(self, character):
        self.characters_speed.pop(character)
        self.party.pop(character)
        self.modifiers.pop(character)

    @staticmethod
    def update_speed(party, characters_speed, modifiers):
        for c in party:
            party[c] += characters_speed[c] + modifiers[c]

    @staticmethod
    def get_next(party):
        fastest = max(party, key=party.get)
        if party[fastest] >= 100:
            return fastest
        elif party[fastest] < 100:
            return None

    @staticmethod
    def reduce_speed(party, character):
        party[character] -= 100

    def get_next_seed(self):
        return QueueModel._get_next_seed(self.party, self.characters_speed, self.modifiers )

    @staticmethod
    def _get_next_seed(party, character_speeds, modifiers):
        party_seed = dict()

        for key, value in party.items():
            party_seed[key] = value

        while True:
            character = QueueModel.get_next(party_seed)
            if character is not None:
                QueueModel.reduce_speed(party_seed, character)
                break
            elif character is None:
                QueueModel.update_speed(party_seed, character_speeds, modifiers)

        return party_seed

    def get_queue(self):
        return QueueModel._get_queue(self.party, self.characters_speed, self.modifiers)

    @staticmethod
    def _get_queue(party, character_speeds, modifiers):
        party_seed = dict()
        queue = list()

        for key, value in party.items():
            party_seed[key] = value

        quantity = 8
        while quantity - len(queue) != 0:
            character = QueueModel.get_next(party_seed)
            if character is not None:
                queue.append(character)
                QueueModel.reduce_speed(party_seed, character)
            elif character is None:
                QueueModel.update_speed(party_seed, character_speeds, modifiers)

        return queue

    def on_script(self):
        if not QueueModel._initialized and BattleLogic._initialized:
            self._initialize()
        else:
            var = self.queue
            pass
