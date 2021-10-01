from game_object.game_object import GameObject


class BaseCard(GameObject):

    def __init__(self):
        super(BaseCard, self).__init__()

        self.card_id = None
        self.card_type = None

    @staticmethod
    def copy(self, obj):
        self.card_id = obj.card_id
        self.card_name = obj.card_name
        self.card_type = obj.card_type


class DescriptiveCard(BaseCard):

    def __init__(self, base):
        super(DescriptiveCard, self).__init__()

        # Copy from base
        # super(DescriptiveCard, self).copy(base)
        BaseCard.copy(self, base)

        self.card_name = None
        self.info_description = None

    @staticmethod
    def copy(self, obj):
        # super(DescriptiveCard, self).copy(obj)
        BaseCard.copy(self, obj)

        self.card_name = obj.card_name
        self.info_description = obj.info_description


class BattleCard(BaseCard):

    def __init__(self, base):
        super(BattleCard, self).__init__()

        # Copy from base
        # super(BattleCard, self).copy(base)
        BaseCard.copy(self, base)

        self.allowed_character_class = list()

        self.action_type = None
        self.base_value = None
        self.multiplier = None
        self.ap_cost = None
        self.energy_cost = None
        self.target = None
        self.caster_status = list()
        self.target_status = list()

    @staticmethod
    def copy(self, obj):
        # super(DescriptiveCard, self).copy(obj)
        BaseCard.copy(self, obj)

        self.allowed_character_class = obj.allowed_character_class
        self.action_type = obj.action_type
        self.base_value = obj.base_value
        self.multiplier = obj.multiplier
        self.ap_cost = obj.ap_cost
        self.energy_cost = obj.energy_cost
        self.target = obj.target
        self.caster_status = obj.caster_status
        self.target_status = obj.target_status


class FullCard(BaseCard):

    def __init__(self, base, desc=None, battle=None):
        super(FullCard, self).__init__()

        # Copy from base
        # super(FullCard, self).copy(base)
        BaseCard.copy(self, base)

        # Copy form desc
        if not desc is None:
            # super(DescriptiveCard, self).copy(desc)
            DescriptiveCard.copy(self, desc)

        # Copy form battle
        if not battle is None:
            # super(BattleCard, self).copy(battle)
            BattleCard.copy(self, battle)

        self.usage_description = None
        self.picture = None
