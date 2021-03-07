from action_types import ActionType


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

    @staticmethod
    def kill_character(target):

        if target.attributes.health <= 0:
            print(target.name.title() + " zostaje zabity!")
