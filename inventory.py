class EquipmentFullException(Exception):
    pass


class Inventory(list):

    def __init__(self, capacity):
        super(Inventory, self).__init__()
        self._capacity = capacity

    def append(self, item):
        if len(self) <= self._capacity:
            return list.append(self, item)
        else:
            raise EquipmentFullException("Equipment Full Exception")

    # def set_capacity(capacity):

    def get_capacity(self):
        return self._capacity