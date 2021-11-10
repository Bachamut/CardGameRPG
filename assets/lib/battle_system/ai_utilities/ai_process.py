from assets.lib.battle_system.action_utilities.action_process import ActionProcess
from assets.lib.battle_system.ai_utilities.ai_preferences import Preferences
from assets.lib.card_utilities.card_manager import CardManager


class AIProcess:

    @staticmethod
    def action_calculation(character, targets):

        cards_values = AIProcess.calculating_cards_values(character, targets)

        best_pairs = dict()

        best_card = None
        best_character = None
        best_value = None

        for it in range(0, (len(cards_values))):

            for card, collection in cards_values.items():

                temp_character = max(collection, key=collection.get)
                temp_value = collection[temp_character]

                if best_value is None or temp_value > best_value:
                    best_card = card
                    best_character = temp_character
                    best_value = temp_value

            best_pairs[best_card] = best_character
            cards_values.pop(best_card, best_character)

            best_value = None

        return best_pairs

    @staticmethod
    def calculating_cards_values(character, targets):

        cards_values = dict()

        preference_matrix = Preferences.get_preferences(character)

        for card in character.hand:

            battle_card = CardManager.create_battle_card(card)
            value_by_targets = AIProcess.card_value_by_affiliation(character, targets, battle_card)

            for target, value_matrix in value_by_targets.items():

                for index, value in enumerate(preference_matrix):
                    value_matrix[index] *= value

                value_by_targets[target] = sum(value_matrix)

            cards_values[card] = value_by_targets

        return cards_values

    @staticmethod
    def card_value_by_affiliation(character, targets, card):

        value_by_targets = dict()

        for target in targets:

            affiliation_matrix = AIProcess.affiliation_matrix(character, target)
            caster_matrix = AIProcess.caster_matrix()

            character_state_matrix = AIProcess.character_state_factor(target)

            card_matrix = AIProcess.card_value_matrix(character, target, card)
            target_status_matrix = AIProcess.target_status_value_calculation(target, card)
            caster_status_matrix = AIProcess.caster_status_value_calculation(target, card)

            for index1, value1 in enumerate(character_state_matrix):
                affiliation_matrix[index1] *= value1

            for index2, value2 in enumerate(affiliation_matrix):
                card_matrix[index2] *= value2
                target_status_matrix[index2] *= value2

            for index3, value3 in enumerate(caster_matrix):
                caster_status_matrix[index3] *= value3

            zipped_lists = zip(card_matrix, target_status_matrix, caster_status_matrix)
            target_sum = [x + y + z for (x, y, z) in zipped_lists]

            value_by_targets[target] = target_sum

        return value_by_targets

    @staticmethod
    def affiliation_matrix(character, target):

        if character.affiliation == "enemy" and target.affiliation == "enemy" or \
                character.affiliation == "ally" and target.affiliation == "ally":

            affiliation_matrix = [-1, 1, 1, -1]

        elif character.affiliation == "enemy" and target.affiliation == "ally" or \
                character.affiliation == "ally" and target.affiliation == "enemy":

            affiliation_matrix = [1, -1, -1, 1]

        return affiliation_matrix

    @staticmethod
    def caster_matrix():

        caster_matrix = [-1, 1, 1, -1]
        return caster_matrix

    @staticmethod
    def card_value_matrix(character, target, card):

        value = ActionProcess.value_calculation(character, target, card)
        if card.card_type == "physical_attack":
            card_matrix = [value, 0, 0, 0]
        if card.card_type == "heal":
            card_matrix = [0, value, 0, 0]
        if card.card_type == "buff" or card.card_type == "skill":
            card_matrix = [0, 0, value, 0]
        if card.card_type == "debuff":
            card_matrix = [0, 0, 0, value]

        return card_matrix

    @staticmethod
    def target_status_value_calculation(target, card):

        return AIProcess._status_value_calculation(target, card.target_status.items())

    @staticmethod
    def caster_status_value_calculation(target, card):

        return AIProcess._status_value_calculation(target, card.caster_status.items())

    @staticmethod
    def _status_value_calculation(target, card_status):

        status_matrix = list()
        sum_value = [0, 0, 0, 0]
        for status_type, parameters in card_status:

            if status_type == "bleed_1":
                status_value = parameters['value'] * parameters['duration'] * 2
                status_matrix = [status_value, 0, 0, 0]
            if status_type == "poison_1":
                status_value = parameters['value'] * parameters['duration'] * 3
                status_matrix = [status_value, 0, 0, 0]
            if status_type == "stun_1":
                status_value = parameters['value'] * parameters['duration'] * 5
                status_matrix = [0, 0, 0, status_value]
            if status_type == "harden_1":
                status_value = parameters['value'] * parameters['duration'] / 5
                status_matrix = [0, 0, status_value, 0]
            if status_type == "regeneration_1":
                status_value = parameters['value'] * parameters['duration'] * 2
                status_matrix = [0, status_value, 0, 0]
            if status_type == "counter_attack_1":
                status_value = parameters['value'] * parameters['duration'] * 2
                status_matrix = [0, 0, status_value, 0]

            zipped_lists = zip(sum_value, status_matrix)
            sum_value = [x + y for (x, y) in zipped_lists]

        return sum_value

    def possible_targets(self):

        targets = list()

        if self.current_character.affiliation == "enemy":
            targets = self.battle_ally
        elif self.current_character.affiliation == "ally":
            targets = self.battle_enemies
        return targets

    def focus_factor(self):

        focus_factor = list()
        targets = self.possible_targets()
        for target in targets:
            health_percentage = (target.battle_attributes.health / target.battle_attributes.health)

            health_factor = health_percentage * (100 - target.battle_attributes.physical_resist) / 100
            focus_factor[target.name] = health_factor

        return focus_factor

    @staticmethod
    def character_state_factor(target):

        character_state_matrix = [1, 1, 1, 1]

        if target.state == "dead":
            character_state_matrix = [0, 0, 0, 0]

        return character_state_matrix
