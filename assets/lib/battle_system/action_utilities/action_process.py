import pygame

from assets.lib.battle_system.action_utilities.action_block import ActionBlock
from assets.lib.battle_system.action_utilities.action_types import ActionType
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.card_utilities.card_model import BaseCard
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.status_utilities.status_model import Status


class ActionProcess:

    @staticmethod
    def action_process(caster, targets, base_card):

        action_scenario = list()

        card = CardManager.create_battle_card(base_card)

        caster.modify_battle_attributes("action_points", -card.ap_cost)

        for target in targets:

            # card.amount = 2

            for it in range(0, card.amount):

                if card.card_type == "physical_attack":
                    action_sequence = ActionProcess.physical_attack(caster, target, card)

                elif card.card_type == "spell":
                    action_sequence = ActionProcess.spell(caster, target, card)

                elif card.card_type == "heal":
                    action_sequence = ActionProcess.heal(caster, target, card)

                elif card.card_type == "skill":
                    action_sequence = ActionProcess.skill(caster, target, card)

                action_scenario += action_sequence

            # Logs.ActionProcessMessage.action_process_info(caster, target, card, value, ActionProcess.action_process.__name__)

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

        # # create action for caster and target
        # caster_action = {card.action_type: value}
        # target_action = {card.action_type: value}
        #
        # print(f'{target.name} - battleHP:{target.battle_attributes.health}')
        # return caster_action, target_action

        return action_scenario

    @staticmethod
    def physical_attack(caster, target, card):

        action_sequence = list()

        value = ActionProcess.value_calculation(caster, target, card)

        if value is not None:
            target.take_damage_battle_attribute(value)

        action_block = ActionBlock(caster, target, card.action_type, value)
        action_sequence.append(action_block)

        for status in target.status_list:
            if status.status_type == "counter_attack_1":

                # TODO There should be card object for "card"

                counter_value = ActionProcess.value_calculation(target, caster, card)
                caster.take_damage_battle_attribute(counter_value)

                action_block = ActionBlock(target, caster, 'counter_attack', counter_value)
                action_sequence.append(action_block)

        return action_sequence

    @staticmethod
    def spell(caster, target, card):

        action_sequence = list()

        for status in target.status_list:
            if status.status_type == "reflect_spell":

                action_block = ActionBlock(caster, target, 'cast_spell')
                action_sequence.append(action_block)

                reflect_value = ActionProcess.value_calculation(target, caster, card)
                caster.take_damage_battle_attribute(reflect_value)

                action_block = ActionBlock(target, caster, 'reflect_spell', reflect_value)
                action_sequence.append(action_block)

            else:
                value = ActionProcess.value_calculation(caster, target, card)
                target.take_damage_battle_attribute(value)
                action_block = ActionBlock(caster, target, card.action_type, value)
                action_sequence.append(action_block)

        return action_sequence

    @staticmethod
    def heal(caster, target, card):

        action_sequence = list()

        value = ActionProcess.value_calculation(caster, target, card)
        target.heal_health_battle_attribute(value)

        action_block = ActionBlock(caster, target, card.action_type, value)
        action_sequence.append(action_block)

        return action_sequence

    @staticmethod
    def skill(caster, target, card):

        action_sequence = list()

        action_block = ActionBlock(caster, target, card.action_type)
        action_sequence.append(action_block)

        return action_sequence

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
        elif card.action_type == 'heal_spell':
            value = ActionType.heal_spell(caster, target, card)
        elif card.action_type == 'self_skill':
            value = ActionType.self_skill(caster, target, card)
        elif card.action_type == 'special_attack':
            value = ActionType.basic_attack(caster, target, card)
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
                ActionProcess.deactivate_status(character, status)
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
        if status.status_type == "counter_attack_1":
            ActionType.status_harden(character, status)
        Logs.ActionProcessMessage.activate_status_info(character, status, ActionProcess.activate_status.__name__)

    @staticmethod
    def deactivate_status(character, status):

        if status.duration == 0:
            if status.status_role == "temporary_modifier":
                Logs.ActionProcessMessage.deactivate_status_info('Dezaktywacja przywraca poprzednie wartości atrybutów', character, status, ActionProcess.deactivate_status.__name__)
            if status.status_role == "permanent_modifier":
                Logs.ActionProcessMessage.deactivate_status_info('Dezaktywacja nic nie zmienia', character, status, ActionProcess.deactivate_status.__name__)
            if status.status_role == "action":
                Logs.ActionProcessMessage.deactivate_status_info('Status nie posiada dezaktywacji', character, status, ActionProcess.deactivate_status.__name__)
        else:
            Logs.ActionProcessMessage.deactivate_status_info('Brak warunku do dezaktywacji', character, status, ActionProcess.deactivate_status.__name__)

    @staticmethod
    def status_expire(character, status):

        if status.duration == 0:
            # remove battle_modifiers related to status
            character.battle_modifiers.remove_related_modifier(status)
            character.remove_status(status)

    @staticmethod
    def restock_action_points(character):

        character.battle_attributes.action_points = character.base_attributes.action_points + character.base_modifiers.action_points

    @staticmethod
    def is_character_dead(character):
        if character.battle_attribute("health") <= 0:
            character.state = "dead"
            print(f'{character.name} nie żyje')

    @staticmethod
    def battle_state(battle_ally, battle_enemies):

        for character in battle_ally + battle_enemies:
            ActionProcess.is_character_dead(character)

        if ActionProcess.battle_lost(battle_ally):
            print('wysłano sygnał "battle_lose')

        elif ActionProcess.battle_won(battle_enemies):
            print(f'wysłano sygnał "battle_won')

        else:
            pass

    @staticmethod
    def battle_lost(battle_ally):

        if any(character.state == "alive" for character in battle_ally):
            Logs.ActionProcessMessage.action_process_simple_info(ActionProcess.battle_lost.__name__, 'jeszcze żyjesz')
        else:
            Logs.ActionProcessMessage.action_process_simple_info(ActionProcess.battle_lost.__name__, 'przegrałeś, wszyscy towarzysze nie żyją')

            emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOST, {"event": "BATTLE_LOST", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            return

    @staticmethod
    def battle_won(battle_enemies):

        if any(character.state == "alive" for character in battle_enemies):
            Logs.ActionProcessMessage.action_process_simple_info(ActionProcess.battle_lost.__name__, 'żywi przeciwnicy, kontynuujesz walkę')
        else:
            Logs.ActionProcessMessage.action_process_simple_info(ActionProcess.battle_lost.__name__, 'wygrałeś, wszyscy przeciwnicy nie żyją')

            emit_signal = pygame.event.Event(BattleLogic.BATTLE_WON, {"event": "BATTLE_WON", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            return

