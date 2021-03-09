class Status():

    @staticmethod
    def add_status(caster, target, card):
        if card.caster_status:
            for key, value in card.caster_status.items():
                if key in caster.status:
                    caster.status[key] = caster.status[key] + value
                else:
                    caster.status[key] = value
        if card.target_status:
            for key, value in card.target_status.items():
                if key in target.status:
                    target.status[key] = target.status[key] + value
                else:
                    target.status[key] = value

    @staticmethod
    def status_stun(character):
        character.attributes.action_points -= character.status['stun']

    @staticmethod
    def status_bleed(character):
        character.attributes.health -= character.status['bleed']
        character.status['bleed'] -= 1
        if character.status['bleed'] == 0:
            del character.status['bleed']

    @staticmethod
    def status_poison(character):
        character.attributes.health -= character.status['poison']
        character.attributes.energy -= character.status['poison']
        character.status['poison'] -= 1
        if character.status['poison'] == 0:
            del character.status['poison']