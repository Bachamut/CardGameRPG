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
    def create_base_card(card_id):
        config = CardManager.card_config[card_id]
        card = BaseCard()

        card.card_id = config['card_id']
        card.card_name = config['card_name'] # TODO: karty powinny być identyfikowanie na podstawie CARD_ID

        return card

    @staticmethod
    def create_descriptive_card(base):
        config = CardManager.card_config[base.card_name] # TODO: karty powinny być identyfikowanie na podstawie CARD_ID
        card = DescriptiveCard(base)

        card.card_name = config['card_name']
        card.info_description = config['description']

        return card

    @staticmethod
    def create_battle_card(base):
        config = CardManager.card_config[base.card_name]
        card = BattleCard(base)

        card.character_class = config['character_class']

        card.action_type = config['action_type']
        card.base_value = config['base_value']
        card.multiplier = config['multiplier']
        card.ap_cost = config['ap_cost']
        card.energy_cost = config['energy_cost']
        card.caster_status = config['caster_status']
        card.target_status = config['target_status']

        return card

    @staticmethod
    def create_full_card(base):
        config = CardManager.card_config[base.card_name]
        card = FullCard(base,
                        CardManager.create_descriptive_card(base),
                        CardManager.create_battle_card(base))

        card.usage_description = config['description']
        # self.picture = config['picture']

        return card
