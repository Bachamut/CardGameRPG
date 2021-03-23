import pygame

from assets.lib.character_model import CharacterModel
from assets.lib.text_line import TextLine
from game_object.game_object import GameObject


class PartyStatusView(GameObject):

    _initialized = False

    def __init__(self):
        super(PartyStatusView, self).__init__()
    def _initialize(self):
        PartyStatusView._initialized = True

        self.add_property("SpriteProperty")
        self.add_property("BlitProperty")
        self.property("SpriteProperty").visible = True
        self.font = pygame.font.Font("assets/DisposableDroidBB.ttf", 32)
        self.property("SpriteProperty").surface = self.font.render("Party Status", True, [0,0,0])

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 10
        self.position.y = 200

    def on_create(self):
        pass

    def on_script(self):
        if not PartyStatusView._initialized and CharacterModel._initialized and len(GameObject.get_object_pool().select_with_label('CharacterModel')) != 0:
            self._initialize()
        else:
            pass

        if PartyStatusView._initialized:
            party = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
            step = 0
            font = pygame.font.Font("assets/DisposableDroidBB.ttf", 22)
            for character in party.party_list:
                line = TextLine.get_instance()
                line.set_font(font)
                line.update(f'{character.name} - HP:{character.attributes.health} EP:{character.attributes.energy}')
                self.attach_child(line)
                line.property('SpriteProperty').visible = True

                position = line.property('TransformProperty').position
                position.y = 40
                position.y += step
                step += 60
                position.x = 0

    def on_signal(self, signal):
        pass