from assets.lib.ui.widget import Widget


class TextLine(Widget):

    def __init__(self, font_face, font_color, text=''):
        super(TextLine, self).__init__()

        self.object_class = 'TextLine'
        self.object_type = "BaseUi"
        self.object_label = 'TextLine'

        self.add_property('SpriteProperty')

        self.set_font(font_face)
        self.font_color = font_color
        self._text = text

    def set_font(self, font_face):

        self.font_face = font_face

        return self

    def update(self, text, color=(0, 0, 0)):

        self._text = str(text)
        self.render()

        return self

    def render(self):

        self.property('SpriteProperty').surface = self.font_face.render(self._text, True, self.font_color)
        self.property('SpriteProperty')._surface = self.property('SpriteProperty').surface

        return self
