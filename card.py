class Card():
    """Define information about card object"""

    def __init__(self):

        self.card_id = None
        self.name = ''
        self.action_type = ''
        self.description = ''
        self.character_class = []
        self.base_value = None
        self.multiplier = None
        self.ap_cost = None
        self.mana_cost = None
        self.caster_status = {}
        self.target_status = {}

    def get_card(self):

        self.card_info = {'card_id': self.card_id,
                          'name': self.name,
                          'action_type': self.action_type,
                          'description': self.description,
                          'character_class': self.character_class,
                          'base_value': self.base_value,
                          'modifiers': self.multiplier,
                          'ap_cost': self.ap_cost,
                          'mana_cost': self.mana_cost,
                          'caster_status': self.caster_status,
                          'target_status': self.target_status,
                          }

        return self.card_info
