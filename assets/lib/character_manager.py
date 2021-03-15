import json

from assets.lib.character import Character


class CharacterManager():

    character_config = {}

    @staticmethod
    def load_config(filename):
        with open(filename, 'r') as file:
            config = json.load(file)
            for key, value in config.items():
                CharacterManager.character_config.update({key: value})

    @staticmethod
    def create_character(key_name):
        config = CharacterManager.character_config[key_name]
        character = Character()

        character.name = config['name']
        character.character_class = config['character_class']
        character.attributes.health = config['health']
        character.attributes.energy = config['energy']
        character.attributes.strength = config['strength']
        character.attributes.dexterity = config['dexterity']
        character.attributes.magic = config['magic']
        character.attributes.stamina = config['stamina']
        character.attributes.physical_resist = config['physical_resist']
        character.attributes.magic_resist = config['magic_resist']

        return character
