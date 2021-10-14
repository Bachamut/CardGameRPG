from game_object.game_object import GameObject


class Widget(GameObject):

    def __init__(self):
        super(Widget, self).__init__()

        self.object_class = "Widget"
        self.object_type = "BaseUi"
        self.object_label = "Widget"

        self.add_property('TransformProperty')
        self.add_property('BlitProperty')

        GameObject.add_new_object(self)
