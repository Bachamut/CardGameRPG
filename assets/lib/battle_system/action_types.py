
# zawiera metody które określają wynik zastosowania danej AKCJI
from assets.lib.battle_system.status import Status
from assets.lib.card_utilities.card import BaseCard
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.status_utilities.status_manager import StatusManager


class ActionType:


    @staticmethod
    def status_expire(character, status_list):

        for index, status in enumerate(status_list):
            if status.duration == 0:
                character.remove_status(status_list[index])
        for status in character.status_list:
            print(f'DURATION: {status.duration}')

    @staticmethod
    def get_status_activation(signal_subtype):

        status_list = list()

        for status_type in StatusManager.status_type_list:
            if status_type.activation == signal_subtype:
                status_list.append(status_type)
        return status_list

    @staticmethod
    def get_status_matched(character, status_type):

        status_activation_list = list()
        for status in status_type:
            for index, st in enumerate(character.status_list):
                if st.status_type == status.status_id:
                    status_activation_list.append(character.status_list[index])
        return status_activation_list

    @staticmethod
    def status_activation(character, status_list):

        for index, st in enumerate(status_list):
            ActionType.apply_status(character, status_list[index])

    @staticmethod
    def apply_status(character, status):

        if status.status_type == "bleed_1":
            ActionType.status_bleed(character, status)
        if status.status_type == "poison_1":
            ActionType.status_poison(character, status)

    @staticmethod
    def status_bleed(character, status):

        status.duration -= 1
        character.base_attributes.health -= status.value

    @staticmethod
    def status_poison(character, status):

        status.duration -= 1
        character.base_attributes.health -= status.value

        if status.value >= 1:
            status.value -= 1

    @staticmethod
    def value_calculation(caster, target, card):

        if isinstance(card, BaseCard):
            card = CardManager.create_battle_card(card)
            print(f'creating battlecard for dmg prediction')
        if card.action_type == 'magic_attack':
            value = ActionType.magic_attack(caster, target, card)
        elif card.action_type == 'basic_attack':
            value = ActionType.basic_attack(caster, target, card)
        elif card.action_type == 'piercing_attack':
            value = ActionType.piercing_attack(caster, target, card)
        elif card.action_type == 'agile_attack':
            value = ActionType.agile_attack(caster, target, card)
        elif card.action_type == 'magic_spell':
            value = ActionType.magic_spell(caster, target, card)
        elif card.action_type == 'bow_attack':
            value = ActionType.bow_attack(caster, target, card)
        return value

    @staticmethod
    def action_process(caster, target, base_card):

        card = CardManager.create_battle_card(base_card)

        # health processing
        value = ActionType.value_calculation(caster, target, card)
        target.base_attributes.health -= value

        # status processing for target
        for status_type, parameters in card.target_status.items():
            status = Status(status_type, parameters['value'], parameters['duration'])

            target.add_status(status)

        # status processing for caster
        for status_type, parameters in card.caster_status.items():
            status = Status(status_type, parameters['value'], parameters['duration'])

            caster.add_status(status)

        # create action for caster and target
        caster_action = {card.action_type: value}
        target_action = {card.action_type: value}

        return caster_action, target_action

    @staticmethod
    def magic_attack(caster, target, card):

        value = (card.base_value + (caster.base_attributes.magic + caster.base_modifiers.magic) * \
                         card.multiplier) * (100 - target.base_attributes.magic_resist) / 100
        return value

    @staticmethod
    def basic_attack(caster, target, card):

        value = (card.base_value + (caster.base_attributes.strength + caster.base_modifiers.strength) * \
                         card.multiplier) * (100 - target.base_attributes.physical_resist) / 100
        return value

    @staticmethod
    def piercing_attack(caster, target, card):

        value = (card.base_value + (caster.base_attributes.strength + caster.base_modifiers.strength) * \
                         card.multiplier)
        return value

    @staticmethod
    def agile_attack(caster, target, card):

        value = (card.base_value + (caster.base_attributes.dexterity + caster.base_modifiers.dexterity) * \
                         card.multiplier) * (100 - target.base_attributes.physical_resist) / 100
        return value

    @staticmethod
    def magic_spell(caster, target, card):

        value = (card.base_value + (caster.base_attributes.magic + caster.base_modifiers.magic) * \
                         card.multiplier) * (100 - target.base_attributes.magic_resist_resist) / 100
        return value

    @staticmethod
    def bow_attack(caster, target, card):

        value = (card.base_value + (caster.base_attributes.dexterity + caster.base_modifiers.dexterity) * \
                         card.multiplier) * (100 - target.base_attributes.physical_resist * 2.0) / 100
        return value

