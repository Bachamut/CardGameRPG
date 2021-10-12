
class AIConditionBlock:

    def __init__(self):

        self.priority = None
        self.subject = None
        self.attribute = None
        self.operator = None
        self.value = None

        self.do_dmg_modifier = None
        self.do_heal_modifier = None
        self.do_buff_modifier = None
        self.do_debuff_modifier = None

    @staticmethod
    def conditional_equation(character, condition_block):
        if condition_block.subject == "self":
            if condition_block.operator == "=":
                if character.battle_attribute(condition_block.attribute) == condition_block.value:
                    print(f'{condition_block.attribute} is equal to {condition_block.value}')

                    return [condition_block.do_dmg_modifier, condition_block.do_heal_modifier, condition_block.do_buff_modifier, condition_block.do_debuff_modifier]

            elif condition_block.operator == ">=":
                if character.battle_attribute(condition_block.attribute) >= condition_block.value:
                    print(f'{condition_block.attribute} is greater than or equal to {condition_block.value}')

                    return [condition_block.do_dmg_modifier, condition_block.do_heal_modifier, condition_block.do_buff_modifier, condition_block.do_debuff_modifier]

            elif condition_block.operator == "<=":
                if character.battle_attribute(condition_block.attribute) <= condition_block.value:
                    print(f'{condition_block.attribute} is less than or equal to {condition_block.value}')

                    return [condition_block.do_dmg_modifier, condition_block.do_heal_modifier, condition_block.do_buff_modifier, condition_block.do_debuff_modifier]

            elif condition_block.operator == ">":
                if character.battle_attribute(condition_block.attribute) > condition_block.value:
                    print(f'{condition_block.attribute} is greater than {condition_block.value}')

                    return [condition_block.do_dmg_modifier, condition_block.do_heal_modifier, condition_block.do_buff_modifier, condition_block.do_debuff_modifier]

            elif condition_block.operator == "<":
                if character.battle_attribute(condition_block.attribute) < condition_block.value:
                    print(f'{condition_block.attribute} is less than {condition_block.value}')

                    return [condition_block.do_dmg_modifier, condition_block.do_heal_modifier, condition_block.do_buff_modifier, condition_block.do_debuff_modifier]

