
class Preferences:

    def __init__(self):

        self.do_dmg = 1
        self.do_heal = 1
        self.do_effect = 1

        self.factor_alpha = 1
        self.factor_beta = 1
        self.factor_gamma = 1

    def update_preferences(self, character):

        health_percentage = (character.current_hp / character.max_hp)

        self.do_dmg = self.do_dmg * health_percentage * self.factor_alpha
        self.do_heal = self.do_heal / health_percentage * self.factor_beta
        self.do_effect = self.do_effect * health_percentage * self.factor_gamma
