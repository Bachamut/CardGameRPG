import json

from item import Item


class ItemManager():

    item_config = {}

    @staticmethod
    def load_config(filename):
        with open(filename, 'r') as file:
            config = json.load(file)
            for key, value in config.items():
                ItemManager.item_config.update({key: value})

    @staticmethod
    def create_item(key_name):
        config = ItemManager.item_config[key_name]
        item = Item()

        item.item_id = config['item_id']
        item.item_name = config['item_name']
        item.item_type = config['item_type']
        item.slot_type = config['slot_type']
        item.description = config['description']
        item.item_value = config['item_value']
        item.required_attributes.health = config['r_health']
        item.required_attributes.mana = config['r_mana']
        item.required_attributes.strength = config['r_strength']
        item.required_attributes.dexterity = config['r_dexterity']
        item.required_attributes.magic = config['r_magic']
        item.required_attributes.stamina = config['r_stamina']
        item.required_attributes.physical_resist = config['r_physical_resist']
        item.required_attributes.magic_resist = config['r_magic_resist']
        item.modifiers.health = config['m_health']
        item.modifiers.mana = config['m_mana']
        item.modifiers.strength = config['m_strength']
        item.modifiers.dexterity = config['m_dexterity']
        item.modifiers.magic = config['m_magic']
        item.modifiers.stamina = config['m_stamina']
        item.modifiers.physical_resist = config['m_physical_resist']
        item.modifiers.magic_resist = config['m_magic_resist']
        item.add_card = config['add_card']

        return item