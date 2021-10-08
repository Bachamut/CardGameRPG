from assets.lib.battle_system.action_utilities.action_types import ActionType
from assets.lib.card_utilities.card_model import BaseCard
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.status_utilities.status_model import Status


class ActionProcess:

    @staticmethod
    def action_process(caster, target, base_card):

        card = CardManager.create_battle_card(base_card)

        # health processing
        value = ActionProcess.value_calculation(caster, target, card)
        target.take_damage(value)
        print(f'{caster.name} używa "{card.card_name}" na {target.name}, zadaje {value} obrażeń!')

        # status processing for target
        for status_type, parameters in card.target_status.items():
            status = Status(status_type, parameters['value'], parameters['duration'])
            status.source = caster.name

            target.add_status(status)
            if status.rate == "instant":
                ActionProcess.activate_status(target, status)

        # status processing for caster
        for status_type, parameters in card.caster_status.items():
            status = Status(status_type, parameters['value'], parameters['duration'])
            status.source = caster.name

            caster.add_status(status)
            if status.rate == "instant":
                ActionProcess.activate_status(caster, status)

        print(f'{caster.name} posiada {len(caster.status_list)} statusów:')

        # create action for caster and target
        caster_action = {card.action_type: value}
        target_action = {card.action_type: value}

        print(f'{target.name} - baseHP:{target.base_attributes.health}')
        return caster_action, target_action

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
    def status_for_activation(character, stage):

        for index, status in enumerate(character.status_list):
            if status.activation == stage:
                if status.duration > 0:
                    ActionProcess.activate_status(character, status)

    @staticmethod
    def status_for_deactivation(character, stage):

        for index, status in enumerate(character.status_list):
            if status.deactivation == stage:
                # ActionProcess.deactivate_status(character, status)
                ActionProcess.status_expire(character, status)

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
        print(f'{character.name}: aktywowano {status.name} (pozostałe duration: {status.duration})')

    @staticmethod
    def deactivate_status(character, status):

        if status.duration == 0:
            if status.status_role == "temporary_modifier":
                print(f'{status.name} przy dezaktywacji przywraca poprzednie wartości')
            if status.status_role == "permanent_modifier":
                print(f'{status.name} przy dezaktywaci nie zmieni nic')
            if status.status_role == "action":
                print(f'{status.name} nie ma dezaktywacji')
        else:
            print(f'Nie ma statusu do dezaktywacji')

    @staticmethod
    def status_expire(character, status):

        if status.duration == 0:
            # remove battle_modifiers related to status
            character.battle_modifiers.remove_related_modifier(status)
            character.remove_status(status)

    @staticmethod
    def restock_action_points(character):

        character.battle_attributes.action_points = character.base_attributes.action_points + character.base_modifiers.action_points

