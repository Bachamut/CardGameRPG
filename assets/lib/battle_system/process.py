from assets.lib.battle_system.action_types import ActionType
from status import Status


class Process():

    @staticmethod
    def action_process(caster, target, card):

        if card.action_type == 'magic_attack':
            ActionType.magic_attack(caster, target, card)
        elif card.action_type == 'basic_attack':
            ActionType.basic_attack(caster, target, card)
        elif card.action_type == 'piercing_attack':
            ActionType.piercing_attack(caster, target, card)
        elif card.action_type == 'agile_attack':
            ActionType.agile_attack(caster, target, card)
        elif card.action_type == 'magic_spell':
            ActionType.magic_spell(caster, target, card)
        elif card.action_type == 'bow_attack':
            ActionType.bow_attack(caster, target, card)

        Status.add_status(caster, target, card)

    @staticmethod
    def kill_character(target):

        if target.attributes.health <= 0:
            print(target.name.title() + " zostaje zabity!")

    @staticmethod
    def apply_status(character):
        if character.status:
            for key, value in character.status.items():
                if key == 'stun':
                    Status.status_stun(character)
                if key == 'bleed':
                    Status.status_bleed(character)
                if key == 'poison':
                    Status.status_poison(character)
    @staticmethod
    def end_turn(character):
        Process.apply_status(character)


