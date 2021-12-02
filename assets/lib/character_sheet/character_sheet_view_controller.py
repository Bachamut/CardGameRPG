
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.ui.container import Container


class CharacterSheetViewController(GameObjectSharedResource):

    def __init__(self):
        super(CharacterSheetViewController).__init__()

        self.sheet_template = [3, 2, 1]
        self.character = None

        self.row_container_list = list()
        self.font_faces = dict()

        interspace = 0
        for row in self.sheet_template:

            row_container = Container()
            # self.attach_child(row_container)
            row_container.property('TransformProperty').position.x = 520 + interspace
            row_container.property('TransformProperty').position.y = 220

            for column in range(row):

                # text_line = TextLine(self.font_faces['open_sans_normal'], (0, 0, 0), f'SKILL').render()

                skill_container = Container()
                # self.attach_child(skill_container)
                skill_container.property('TransformProperty').position.x = 40
                skill_container.property('TransformProperty').position.y = 20 + interspace
                # skill_container.attach_child(text_line)

            interspace += 40
