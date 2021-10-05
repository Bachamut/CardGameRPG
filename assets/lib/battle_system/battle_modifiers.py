
class BattleModifiers:

    @property
    def health(self):
        return self._get_modifier_sum("health")

    @property
    def max_health(self):
        return self._get_modifier_sum("max_health")

    @property
    def energy(self):
        return self._get_modifier_sum("energy")

    @property
    def max_energy(self):
        return self._get_modifier_sum("max_energy")

    @property
    def action_points(self):
        return self._get_modifier_sum("action_points")

    @property
    def strength(self):
        return self._get_modifier_sum("strength")

    @property
    def dexterity(self):
        return self._get_modifier_sum("dexterity")

    @property
    def stamina(self):
        return self._get_modifier_sum("stamina")

    @property
    def magic(self):
        return self._get_modifier_sum("magic")

    @property
    def speed(self):
        return self._get_modifier_sum("speed")

    @property
    def physical_resist(self):
        return self._get_modifier_sum("physical_resist")

    @property
    def magic_resist(self):
        return self._get_modifier_sum("magic_resist")

    def __init__(self):

        self._modifiers = list()

    def add_modifier(self, modifier):

        self._modifiers.append(modifier)

    def _get_modifier_sum(self, attribute):

        result = 0

        for modifier in self._modifiers:

            if modifier.attribute == attribute:
                result += modifier.value

        return result

    def remove_related_modifier(self, status):

        for modifier in self._modifiers:

            if modifier._related_status == status:
                self._modifiers.remove(modifier)
