
class QueueModel:

    def __init__(self):
        self.characters_speed = dict()
        self.modifiers = dict()
        self.party = dict()

    def setup_queue(self, units):
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

    @staticmethod
    def get_next_seed(party, character_speeds, modifiers):
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

    @staticmethod
    def get_queue(party, character_speeds, modifiers):
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
