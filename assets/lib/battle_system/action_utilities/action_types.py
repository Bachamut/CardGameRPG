# zawiera metody które określają wynik zastosowania danej AKCJI

class ActionType:


    # Statuses definition
    @staticmethod
    def status_bleed(character, status):

        status.duration -= 1
        # character.take_damage(status.value)
        character.modify_battle_attributes("health", -status.value)

    @staticmethod
    def status_poison(character, status):

        status.duration -= 1
        # character.take_damage(status.value)
        character.modify_battle_attributes("health", -status.value)

        if status.value >= 1:
            status.value -= 1

    @staticmethod
    def status_stun(character, status):

        # status.duration -= 1
        # character.modify_battle_modifiers("action_points", -status.value)

        # TODO: Uncomment this after debug
        status.duration -= 1
        character.modify_battle_modifiers("strength", -status.value, status)

    @staticmethod
    def status_harden(character, status):

        status.duration -= 1
        character.modify_battle_modifiers("physical_resist", status.value, status)

    @staticmethod
    def counter_attack_1(character, status):

        status.duration -= 1

    # Action types definition
    @staticmethod
    def basic_attack(caster, target, card):

        value = (card.base_value + ((caster.battle_attributes.strength + caster.battle_modifiers.strength) *
                                    card.multiplier)) * (100 - (target.battle_attributes.physical_resist +
                                                                target.battle_modifiers.physical_resist)) / 100

        return value

    @staticmethod
    def piercing_attack(caster, target, card):

        value = card.base_value + (caster.battle_attribute("strength") * card.multiplier)
        return value

    @staticmethod
    def agile_attack(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("dexterity") * card.multiplier)) * \
                (100 - target.battle_attribute("physical_resist")) / 100
        return value

    @staticmethod
    def magic_attack(caster, target, card):

        value = (card.base_value + caster.battle_attribute("magic") * card.multiplier) * \
                (100 - target.battle_attribute("magic_resist")) / 100
        return value

    @staticmethod
    def magic_spell(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("magic") * card.multiplier)) * \
                (100 - target.battle_attribute("magic_resist")) / 100
        return value

    @staticmethod
    def bow_attack(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("dexterity") * card.multiplier)) * \
                (100 - target.battle_attribute("physical_resist") * 2.0) / 100
        return value

    @staticmethod
    def heal_spell(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("magic") * card.multiplier))
        return value

    @staticmethod
    def self_skill(caster, target, card):

        value = 0

        return value



