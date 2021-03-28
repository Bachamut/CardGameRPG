import pygame

from assets.lib.character_model import CharacterModel
from assets.lib.text_line import TextLine
from game_object.game_object import GameObject
from lib.battle_logic import STATUS_UPDATE_SIGNAL, STATUS_RESET_SIGNAL


class PartyView(GameObject):

    _initialized = False

    def __init__(self):
        super(PartyView, self).__init__()
        self.ally = None
        self.characters_status = None

    def _initialize(self):
        PartyView._initialized = True
        self.ally = GameObject.get_object_pool().select_with_label('CharacterModel')[0].ally

        self.add_property("SpriteProperty")
        self.add_property("BlitProperty")
        self.property("SpriteProperty").visible = True
        self.font_32 = pygame.font.Font("assets/DisposableDroidBB.ttf", 32)
        self.property("SpriteProperty").surface = self.font_32.render("Party", True, [0, 0, 0])

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 10
        self.position.y = 200

        # Configure section description and TextLine for each character in ally
        self.font_22 = pygame.font.Font("assets/DisposableDroidBB.ttf", 22)

        self.setup_party()

    def setup_party(self):
        self.characters_status = list()
        step = 0
        for character in self.ally:
            line = TextLine.get_instance()
            line.set_font(self.font_22)
            line.property('SpriteProperty').visible = True

            position = line.property('TransformProperty').position
            position.y = 40
            position.y += step
            step += 60
            position.x = 0

            self.attach_child(line)
            self.characters_status.append(line)

        for line in self.characters_status:
            index = self.characters_status.index(line)
            line.update(
                f'{self.ally[index].name} - HP:{self.ally[index].attributes.health} EP:{self.ally[index].attributes.energy}')

    def on_create(self):
        pass

    def on_script(self):
        if not PartyView._initialized and CharacterModel._initialized:
            self._initialize()
        else:
            pass

    def on_signal(self, signal):
        if PartyView._initialized:
            if signal.type == STATUS_RESET_SIGNAL:
                self.setup_party()
            if signal.type == STATUS_UPDATE_SIGNAL:
                for line in self.characters_status:
                    index = self.characters_status.index(line)
                    line.update(f'{self.ally[index].name} - HP:{self.ally[index].attributes.health} EP:{self.ally[index].attributes.energy}')
