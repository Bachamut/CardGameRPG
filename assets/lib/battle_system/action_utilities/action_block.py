class ActionBlock:

    def __init__(self, caster, target, action_type, value=None):

        self.caster = caster
        self.target = target
        self.action_type = action_type
        self.value = value
