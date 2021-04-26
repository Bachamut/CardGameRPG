from game_object.game_object import GameObject


class TextLine(GameObject):

    def __init__(self):
        super(TextLine, self).__init__()

    @staticmethod
    def get_instance():
        gobject = TextLine()

        gobject.object_class = 'TextLine'
        gobject.object_label = 'TextLine'

        gobject.add_property('TransformProperty')
        gobject.add_property('BlitProperty')
        gobject.add_property('SpriteProperty')

        GameObject.add_new_object(gobject)

        return gobject

    def set_font(self, font):
        self.font = font

    def update(self, text, color=(0, 0, 0)):
        self.text = str(text)
        self.property('SpriteProperty').surface = self.font.render(self.text, True, color)
