import json

from assets.lib.character_utilities.character_model import BaseCharacter


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
        character.character_type = config['character_type']
        character.affiliation = config['affiliation']

        character.base_attributes.health = config['health']
        character.base_attributes.max_heath = config['health']
        character.base_attributes.energy = config['energy']
        character.base_attributes.max_energy = config['energy']
        character.base_attributes.action_points = config['action_points']

        character.base_attributes.strength = config['strength']
        character.base_attributes.dexterity = config['dexterity']
        character.base_attributes.magic = config['magic']
        character.base_attributes.speed = config['speed']
        character.base_attributes.stamina = config['stamina']

        character.base_attributes.physical_resist = config['physical_resist']
        character.base_attributes.magic_resist = config['magic_resist']

        character.preferences.do_dmg = config['do_dmg']
        character.preferences.do_heal = config['do_heal']
        character.preferences.do_effect = config['do_effect']
        character.preferences.factor_alpha = config['factor_alpha']
        character.preferences.factor_beta = config['factor_beta']
        character.preferences.factor_gamma = config['factor_gamma']

        return character
