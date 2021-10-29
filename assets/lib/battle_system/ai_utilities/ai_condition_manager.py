import json

from assets.lib.battle_system.ai_utilities.ai_condition_model import AIConditionBlock


class AIConditionManager:

    condition_config = dict()

    @staticmethod
    def load_config(filename):

        with open(filename, 'r') as file:
            config = json.load(file)
            for key, value in config.items():
                AIConditionManager.condition_config.update({key: value})

    @staticmethod
    def create_condition_blocks(character):

        condition_collection = AIConditionManager.condition_config[character.name]

        if condition_collection is None:
            pass

        else:
            for block, properties in condition_collection.items():

                condition_block = AIConditionBlock()

                condition_block.priority = properties["priority"]
                condition_block.subject = properties["subject"]
                condition_block.attribute = properties["attribute"]
                condition_block.operator = properties["operator"]
                condition_block.value = properties["value"]
                condition_block.do_dmg_modifier = properties["do_dmg_modifier"]
                condition_block.do_heal_modifier = properties["do_heal_modifier"]
                condition_block.do_buff_modifier = properties["do_buff_modifier"]
                condition_block.do_debuff_modifier = properties["do_debuff_modifier"]

                character.preferences.condition_blocks.append(condition_block)


