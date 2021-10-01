
class Attributes:

    def __init__(self):

        self.health = 0
        self.max_health = 0
        self.energy = 0
        self.max_energy = 0
        self.action_points = 0
        self.strength = 0
        self.dexterity = 0
        self.stamina = 0
        self.magic = 0
        self.speed = 0
        self.physical_resist = 0
        self.magic_resist = 0

    @staticmethod
    def compare_attributes(attribute_first, attribute_second):
        f = attribute_first
        s = attribute_second
        result = Attributes()
        result.health = f.health - s.health
        result.energy = f.energy - s.energy
        result.action_points = f.action_points - s.action_points
        result.strength = f.strength - s.strength
        result.dexterity = f.dexterity - s.dexterity
        result.stamina = f.stamina - s.stamina
        result.magic = f.magic - s.magic
        result.speed = f.speed - s.speed
        result.physical_resist = f.physical_resist - s.physical_resist
        result.magic_resist = f.magic_resist - s.magic_resist

        return result
