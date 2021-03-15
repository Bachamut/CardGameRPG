import json

from assets.lib.card import Card


class CardManager():

    card_config = {}

    @staticmethod
    def load_config(filename):
        with open(filename, 'r') as file:
            config = json.load(file)
            for key, value in config.items():
                CardManager.card_config.update({key: value})

    @staticmethod
    def create_card(key_name):
        config = CardManager.card_config[key_name]
        card = Card()

        card.card_id = config['card_id']
        card.card_name = config['card_name']
        card.action_type = config['action_type']
        card.description = config['description']
        card.character_class = config['character_class']
        card.base_value = config['base_value']
        card.multiplier = config['multiplier']
        card.ap_cost = config['ap_cost']
        card.energy_cost = config['energy_cost']
        card.caster_status = config['caster_status']
        card.target_status = config['target_status']

        return card
