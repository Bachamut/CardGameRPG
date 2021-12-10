import json

from assets.lib.card_utilities.card_model import BaseCard, DescriptiveCard, BattleCard, FullCard


class CardManager:

    card_config = dict()

    @staticmethod
    def load_config(filename):

        with open(filename, 'r') as file:
            config = json.load(file)
            for key, value in config.items():
                CardManager.card_config.update({key: value})

    @staticmethod
    def create_base_card(key):

        config = CardManager.card_config[key]
        card = BaseCard()

        card.card_id = config['card_id']
        card.card_name = config['card_name']
        card.card_type = config['card_type']

        return card

    @staticmethod
    def create_descriptive_card(base_base):

        config = CardManager.card_config[base_base.card_id]
        descriptive_card = DescriptiveCard(base_base)

        descriptive_card.card_name = config['card_name']
        descriptive_card.info_description = config['description']

        return descriptive_card

    @staticmethod
    def create_battle_card(base_base):

        config = CardManager.card_config[base_base.card_id]
        battle_card = BattleCard(base_base)

        battle_card.character_class = config['character_class']

        battle_card.action_type = config['action_type']
        battle_card.amount = config['amount']
        battle_card.base_value = config['base_value']
        battle_card.attribute_multiplier = config['attribute_multiplier']
        battle_card.ap_cost = config['ap_cost']
        battle_card.energy_cost = config['energy_cost']
        battle_card.target = config['target']
        battle_card.caster_status = config['caster_status']
        battle_card.target_status = config['target_status']

        return battle_card

    @staticmethod
    def create_full_card(base_base):

        config = CardManager.card_config[base_base.card_id]
        full_card = FullCard(base_base,
                        CardManager.create_descriptive_card(base_base),
                        CardManager.create_battle_card(base_base))

        full_card.usage_description = config['description']
        full_card.resource_name = config['resource']

        return full_card
