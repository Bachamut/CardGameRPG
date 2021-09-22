
# zawiera metody które określają wynik zastosowania danej AKCJI
from assets.lib.status_utilities.status import Status
from assets.lib.card_utilities.card import BaseCard
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.status_utilities.status_manager import StatusManager


class ActionType:

    @staticmethod
    def status_expire(character, status):

        if status.duration == 0:
            character.remove_status(status)
            for status in character.status_list:
                print(f' {status.name}: duration = {status.duration}')

    @staticmethod
    def status_for_activation(character, stage):

        for index, status in enumerate(character.status_list):
            if status.activation == stage:
                if status.duration > 0:
                    ActionType.activate_status(character, status)

    @staticmethod
    def status_for_deactivation(character, stage):

        for index, status in enumerate(character.status_list):
            if status.deactivation == stage:
                ActionType.deactivate_status(character, status)
                ActionType.status_expire(character, status)

        print(f'{character.name} posiada {len(character.status_list)} statusów:')

    @staticmethod
    def deactivate_status(character, status):

        if status.duration == 0:
            if status.status_role == "temporary_modifier":
                print(f'{status.name} przy deaktywacji przywraca poprzednie wartości')
            if status.status_role == "permanent_modifier":
                print(f'{status.name} przy deaktywaci nie zmieni nic')
            if status.status_role == "action":
                print(f'{status.name} nie ma deaktywacji')
        else:
            print(f'Nie ma statusu do deaktywacji')

    @staticmethod
    def activate_status(character, status):

        if status.status_type == "bleed_1":
            ActionType.status_bleed(character, status)
        if status.status_type == "poison_1":
            ActionType.status_poison(character, status)
        if status.status_type == "stun_1":
            ActionType.status_stun(character, status)
        if status.status_type == "harden_1":
            ActionType.status_harden(character, status)

    # Statuses definition
    @staticmethod
    def status_bleed(character, status):

        status.duration -= 1
        character.take_damage(status.value)

    @staticmethod
    def status_poison(character, status):

        status.duration -= 1
        character.take_damage(status.value)

        if status.value >= 1:
            status.value -= 1

    @staticmethod
    def status_stun(character, status):

        status.duration -= 1
        character.modify_battle_modifiers("action_points", -status.value)

    @staticmethod
    def status_harden(character, status):

        status.duration -= 1
        character.modify_battle_modifiers("physical_resist", status.value)

    @staticmethod
    def value_calculation(caster, target, card):

        if isinstance(card, BaseCard):
            card = CardManager.create_battle_card(card)
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
        target.take_damage(value)
        # target.base_attributes.health -= value

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

        value = (card.base_value + caster.battle_attribute("strength") * \
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

