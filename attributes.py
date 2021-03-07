class Attributes():

    def __init__(self):

        self.health = 0
        self.mana = 0
        self.action_points = 3
        self.strength = 0
        self.dexterity = 0
        self.stamina = 0
        self.magic = 0
        self.physical_resist = 0
        self.magic_resist = 0

    @staticmethod
    def compare_attributes(attribute_first, attribute_second):

        result = Attributes()
        result.health = attribute_first.health - attribute_second.health
        result.mana = attribute_first.mana - attribute_second.mana
        result.action_points = attribute_first.action_points - attribute_second.action_points
        result.strength = attribute_first.strength - attribute_second.strength
        result.dexterity = attribute_first.dexterity - attribute_second.dexterity
        result.stamina = attribute_first.stamina - attribute_second.stamina
        result.magic = attribute_first.magic - attribute_second.magic
        result.physical_resist = attribute_first.physical_resist - attribute_second.physical_resist
        result.magic_resist = attribute_first.magic_resist - attribute_second.magic_resist

        return result
