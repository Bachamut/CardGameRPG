import json

from assets.lib.character_utilities.character import BaseCharacter


class CharacterManager:

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
        character = BaseCharacter()

        character.name = config['name']
        character.character_class = config['character_class']
        character.base_attributes.health = config['health']
        character.base_attributes.energy = config['energy']
        character.base_attributes.strength = config['strength']
        character.base_attributes.dexterity = config['dexterity']
        character.base_attributes.magic = config['magic']
        character.base_attributes.speed = config['speed']
        character.base_attributes.stamina = config['stamina']
        character.base_attributes.physical_resist = config['physical_resist']
        character.base_attributes.magic_resist = config['magic_resist']

        return character
