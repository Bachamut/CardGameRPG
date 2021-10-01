# zawiera metody które określają wynik zastosowania danej AKCJI

class ActionType:


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

    # Action types definition
    @staticmethod
    def basic_attack(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("strength") * \
                         card.multiplier)) * (100 - target.battle_attribute("physical_resist")) / 100
        return value

    @staticmethod
    def piercing_attack(caster, target, card):

        value = card.base_value + (caster.battle_attribute("strength") * \
                         card.multiplier)
        return value

    @staticmethod
    def agile_attack(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("dexterity") * \
                         card.multiplier)) * (100 - target.battle_attribute("physical_resist")) / 100
        return value

    @staticmethod
    def magic_attack(caster, target, card):

        value = (card.base_value + caster.battle_attribute("magic") * \
                         card.multiplier) * (100 - target.battle_attribute("magic_resist")) / 100
        return value

    @staticmethod
    def magic_spell(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("magic") * \
                         card.multiplier)) * (100 - target.battle_attribute("magic_resist")) / 100
        return value

    @staticmethod
    def bow_attack(caster, target, card):

        value = (card.base_value + (caster.battle_attribute("dexterity") * \
                         card.multiplier)) * (100 - target.battle_attribute("physical_resist") * 2.0) / 100
        return value

