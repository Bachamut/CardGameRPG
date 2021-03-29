
class InventoryFullException(Exception):
    pass


class Inventory(dict):

    def __init__(self, capacity):
        super(Inventory, self).__init__()
        self._capacity = capacity

    def add_item(self, key_name, quantity=1):
        if sum(self.values()) < self._capacity:
            if key_name in self:
                self[key_name] += quantity
            else:
                self[key_name] = quantity
        else:
            raise InventoryFullException("Inventory Full Exception")

    def remove_item(self, key_name, quantity=1):
        # remove item form inventory
        if key_name in self:
            self[key_name] -= quantity
            if self[key_name] <= 0:
                del self[key_name]

    # def set_capacity(capacity):

    def get_capacity(self):
        return self._capacity
