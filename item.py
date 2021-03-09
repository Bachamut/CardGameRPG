from attributes import Attributes


class NoCardInItemException(Exception):
    pass


class Item():
    """Define information about game item"""

    def __init__(self):
        self.item_id = None
        self.item_name = ''
        self.item_type = ''
        self.slot_type = ''
        self.description = ''
        self.item_value = None
        self.required_attributes = Attributes()
        self.modifiers = Attributes()
        self.add_card = []


    def get_card(self):
        if self.add_card:
            return self.add_card
        else:
            raise NoCardInItemException("No Card In Item Exception")

    def set_item(self,
                 item_id,
                 item_name,
                 item_type,
                 slot_type,
                 description,
                 item_value):

        self.item_id = item_id
        self.item_name = item_name
        self.item_type = item_type
        self.slot_type = slot_type
        self.description = description
        self.item_value = item_value
        self.required_attributes = Attributes()
        self.modifiers = Attributes()
        self.add_card = []
