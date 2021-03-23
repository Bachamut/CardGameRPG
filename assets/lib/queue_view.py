import pygame

from assets.lib.battle_logic import CHARACTER_CHANGED
from assets.lib.character_model import CharacterModel
from assets.lib.text_line import TextLine
from game_object.game_object import GameObject


class QueueView(GameObject):

    _initialized = False

    def __init__(self):
        super(QueueView, self).__init__()

    def _initialize(self):
        QueueView._initialized = True

        self.add_property("SpriteProperty")
        self.add_property("BlitProperty")
        self.property("SpriteProperty").visible = True
        self.font = pygame.font.Font("assets/DisposableDroidBB.ttf", 16)
        self.property("SpriteProperty").surface = self.font.render("Turn Queue", True, [0,0,0])

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 400
        self.position.y = 20

        BattleLogic = GameObject.get_object_pool().select_with_label('BattleLogic')[0]
        font = pygame.font.Font("assets/DisposableDroidBB.ttf", 16)
        self.line = TextLine.get_instance()
        self.line.set_font(font)
        self.line.update(f'{BattleLogic.current_character.name}')
        self.attach_child(self.line)
        self.line.property('SpriteProperty').visible = True
        position = self.line.property('TransformProperty').position
        position.y = 40
        position.x = 0

        self.line_current_char = TextLine.get_instance()
        self.line_current_char.set_font(font)
        self.line_current_char.update(f'{BattleLogic.current_character.name}')
        self.attach_child(self.line_current_char)
        self.line_current_char.property('SpriteProperty').visible = True
        position = self.line_current_char.property('TransformProperty').position
        position.y = 16
        position.x = 0



    def on_create(self):
        pass

    def on_script(self):
        if not QueueView._initialized and CharacterModel._initialized and len(GameObject.get_object_pool().select_with_label('CharacterModel')) != 0:
            self._initialize()
        else:
            pass

    def on_signal(self, signal):
        if signal.type == CHARACTER_CHANGED:
            CharacterModel = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
            BattleLogic = GameObject.get_object_pool().select_with_label('BattleLogic')[0]
            line = ''
            self.line_current_char.update(f'Current Character: {BattleLogic.current_character.name}')
            for character in CharacterModel.queue_list:
                line += character.name + ', '
            self.line.update(f'Next: {line}')


