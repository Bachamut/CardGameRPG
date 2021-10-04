
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

    def __add__(self, attribute):

        result = Attributes()

        result.health = self.health + attribute.health
        result.max_health = self.max_health + attribute.max_health
        result.energy = self.energy + attribute.energy
        result.max_energy = self.max_energy + attribute.max_energy
        result.action_points = self.action_points + attribute.action_points
        result.strength = self.strength + attribute.strength
        result.dexterity = self.dexterity + attribute.dexterity
        result.stamina = self.stamina + attribute.stamina
        result.magic = self.magic + attribute.magic
        result.speed = self.speed + attribute.speed
        result.physical_resist = self.physical_resist + attribute.physical_resist
        result.magic_resist = self.magic_resist + attribute.magic_resist

        return result

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
