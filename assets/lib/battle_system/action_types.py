
class ActionType:

    @staticmethod
    def set_status(card):

        if card.target_status:
            for key, value in card.target_status.items():
                status_name = key
                status_duration = int(value)
                print(f'status: {status_name} - {status_duration}')

    @staticmethod
    def magic_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.attributes.magic + caster.modifiers.magic) * \
                         card.multiplier * (100 - target.attributes.magic_resist_resist) / 100
        target.attributes.health -= ActionType.dmg
        caster.attributes.action_points -= card.ap_cost

    @staticmethod
    def basic_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.attributes.strength + caster.modifiers.strength) * \
                         card.multiplier * (100 - target.attributes.physical_resist) / 100
        target.attributes.health -= ActionType.dmg
        caster.attributes.action_points -= card.ap_cost

    @staticmethod
    def piercing_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.attributes.strength + caster.modifiers.strength) * \
                         card.multiplier
        target.attributes.health -= ActionType.dmg
        caster.attributes.action_points -= card.ap_cost

    @staticmethod
    def agile_attack(caster, target, card):

        ActionType.dmg = card.take().base_value + (caster.take().attributes.dexterity + caster.take().modifiers.dexterity) * \
                         card.take().multiplier * (100 - target.take().attributes.physical_resist) / 100
        target.take().attributes.health -= ActionType.dmg
        caster.take().attributes.action_points -= card.take().ap_cost

    @staticmethod
    def magic_spell(caster, target, card):

        ActionType.dmg = card.base_value + (caster.attributes.magic + caster.modifiers.magic) * \
                         card.multiplier * (100 - target.attributes.magic_resist_resist) / 100
        target.attributes.health -= ActionType.dmg
        caster.attributes.action_points -= card.ap_cost

    @staticmethod
    def bow_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.attributes.dexterity + caster.modifiers.dexterity) * \
                         card.multiplier * (100 - target.attributes.physical_resist * 2.0) / 100
        target.attributes.health -= ActionType.dmg
        caster.attributes.action_points -= card.ap_cost
