from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.ui.widget import Widget


class TextBox(Widget):

    def __init__(self, font_face, font_color=(0, 0, 0)):
        super(TextBox, self).__init__()

        self.object_class = "TextBox"
        self.object_type = "BaseUi"
        self.object_label = "TextBox"

        self._text = None
        self._text_lines = list()

        self.font_face = font_face
        self.font_color = font_color
        self.interline = 28


    def set_font(self, font_face):

        self.font_face = font_face

        return self

    def update(self, text, font_color=(0, 0, 0)):

        if self.has_children():

            for child in self.get_children():

                self.detach_child(child)
                child.on_destroy()

        self._text_lines.clear()
        self._text = str(text)
        self.font_color = font_color

        for line_index, tx in enumerate(self._text.split('\n')):
            text_line = TextLine(self.font_face, self.font_color, tx)
            text_line.property('TransformProperty').position.y = self.interline * line_index

            self._text_lines.append(text_line)
            self.attach_child(text_line)
            text_line.render()

        # self.property('SpriteProperty').surface = self.font_face.render(self.text, True, color)

        return self
