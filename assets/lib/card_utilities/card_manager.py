import json

from assets.lib.card_utilities.card import BaseCard, DescriptiveCard, BattleCard, FullCard


class CardManager:

    card_config = {}

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
    def create_descriptive_card(base):
        config = CardManager.card_config[base.card_id]
        card = DescriptiveCard(base)

        card.card_name = config['card_name']
        card.info_description = config['description']

        return card

    @staticmethod
    def create_battle_card(base):
        config = CardManager.card_config[base.card_id]
        card = BattleCard(base)

        card.character_class = config['character_class']

        card.action_type = config['action_type']
        card.base_value = config['base_value']
        card.multiplier = config['multiplier']
        card.ap_cost = config['ap_cost']
        card.energy_cost = config['energy_cost']
        card.target = config['target']
        card.caster_status = config['caster_status']
        card.target_status = config['target_status']

        return card

    @staticmethod
    def create_full_card(base):
        config = CardManager.card_config[base.card_id]
        card = FullCard(base,
                        CardManager.create_descriptive_card(base),
                        CardManager.create_battle_card(base))

        card.usage_description = config['description']
        # self.picture = config['picture']

        return card
