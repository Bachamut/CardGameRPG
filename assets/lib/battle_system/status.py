
class Status:

    # metoda dodaje status z użytej CARD(ACTION) do słownika statusów danego CHARACTER
    @staticmethod
    def add_status(caster, target, card):
        if card.caster_status:
            for key, value in card.caster_status.items():
                if key in caster.status_list:
                    caster.status_list[key] += value
                else:
                    caster.status_list[key] = value
        if card.target_status:
            for key, value in card.target_status.items():
                if key in target.status_list:
                    target.status_list[key] += value
                else:
                    target.status_list[key] = value

    @staticmethod
    def status_stun(character):
        character.base_attributes.action_points -= character.status_list['stun']

    @staticmethod
    def status_bleed(character):
        character.base_attributes.health -= character.status_list['bleed']
        character.status_list['bleed'] -= 1
        if character.status_list['bleed'] == 0:
            del character.status_list['bleed']

    @staticmethod
    def status_poison(character):
        character.base_attributes.health -= character.status_list['poison']
        character.base_attributes.energy -= character.status_list['poison']
        character.status_list['poison'] -= 1
        if character.status_list['poison'] == 0:
            del character.status_list['poison']