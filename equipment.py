class Equipment(dict):

    def __init__(self):
        super(Equipment, self).__init__()

        super().__setitem__('head', None)
        super().__setitem__('hand_l', None)
        super().__setitem__('hand_r', None)
        super().__setitem__('chest', None)
        super().__setitem__('belt', None)
        super().__setitem__('feet', None)
        super().__setitem__('accessory_1', None)
        super().__setitem__('accessory_2', None)
        super().__setitem__('ring_1', None)
        super().__setitem__('ring_2', None)
        super().__setitem__('necklace', None)
