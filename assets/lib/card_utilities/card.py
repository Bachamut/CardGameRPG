from game_object.game_object import GameObject


class Card(GameObject):
    """Define information about card object"""

    def __init__(self):
        super(Card, self).__init__()

        self.card_id = None
        self.card_name = ''
        self.action_type = ''
        self.description = ''
        self.character_class = []
        self.base_value = None
        self.multiplier = None
        self.ap_cost = None
        self.mana_cost = None
        self.caster_status = {}
        self.target_status = {}

        self.selected = False
        self.current = False

    def on_create(self):
        pass

    def get_card(self):

        self.card_info = {'card_id': self.card_id,
                          'name': self.card_name,
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
