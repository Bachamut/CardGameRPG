from assets.lib.battle_system.ai_utilities.ai_condition_model import AIConditionBlock


class Preferences:

    def __init__(self):

        self.do_dmg = None
        self.do_heal = None
        self.do_buff = None
        self.do_debuff = None

        self.condition_blocks = list()

    @staticmethod
    def get_preferences(character):

        preferences_modifier_matrix = Preferences.update_preferences(character)

        default_preferences_matrix = [character.preferences.do_dmg, character.preferences.do_heal, character.preferences.do_buff, character.preferences.do_debuff]

        preferences_matrix = [0, 0, 0, 0]

        for index, value in enumerate(default_preferences_matrix):

            preferences_matrix[index] = value * preferences_modifier_matrix[index]

        print(f'\tpreference matrix:{preferences_matrix}\n\tpreference modifier:{preferences_modifier_matrix}')
        return preferences_matrix

    @staticmethod
    def update_preferences(character):

        for condition_block in character.preferences.condition_blocks:

            preferences_modifier_matrix = AIConditionBlock.conditional_equation(character, condition_block)
            if preferences_modifier_matrix:
                return preferences_modifier_matrix

        return [1.0, 1.0, 1.0, 1.0]

