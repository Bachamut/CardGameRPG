
# zawiera metody które określają wynik zastosowania danej AKCJI
class ActionType:

    # placeholder?
    @staticmethod
    def set_status(card):

        if card.target_status:
            for key, value in card.target_status.items():
                status_name = key
                status_duration = int(value)
                print(f'status: {status_name} - {status_duration}')

    @staticmethod
    def magic_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.base_attributes.magic + caster.base_modifiers.magic) * \
                         card.multiplier * (100 - target.base_attributes.magic_resist) / 100
        target.base_attributes.health -= ActionType.dmg
        caster.base_attributes.action_points -= card.ap_cost

    @staticmethod
    def basic_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.base_attributes.strength + caster.base_modifiers.strength) * \
                         card.multiplier * (100 - target.base_attributes.physical_resist) / 100
        target.base_attributes.health -= ActionType.dmg
        caster.base_attributes.action_points -= card.ap_cost

    @staticmethod
    def piercing_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.base_attributes.strength + caster.base_modifiers.strength) * \
                         card.multiplier
        target.base_attributes.health -= ActionType.dmg
        caster.base_attributes.action_points -= card.ap_cost

    @staticmethod
    def agile_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.base_attributes.dexterity + caster.base_modifiers.dexterity) * \
                         card.multiplier * (100 - target.base_attributes.physical_resist) / 100
        target.base_attributes.health -= ActionType.dmg
        caster.base_attributes.action_points -= card.ap_cost

    @staticmethod
    def magic_spell(caster, target, card):

        ActionType.dmg = card.base_value + (caster.base_attributes.magic + caster.base_modifiers.magic) * \
                         card.multiplier * (100 - target.base_attributes.magic_resist_resist) / 100
        target.base_attributes.health -= ActionType.dmg
        caster.base_attributes.action_points -= card.ap_cost

    @staticmethod
    def bow_attack(caster, target, card):

        ActionType.dmg = card.base_value + (caster.base_attributes.dexterity + caster.base_modifiers.dexterity) * \
                         card.multiplier * (100 - target.base_attributes.physical_resist * 2.0) / 100
        target.base_attributes.health -= ActionType.dmg
        caster.base_attributes.action_points -= card.ap_cost
