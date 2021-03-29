import pygame

from assets.lib.character_model import CharacterModel
from assets.lib.text_line import TextLine
from assets.lib.battle_logic import BattleLogic
from game_object.game_object import GameObject

class QueueView(GameObject):

    _initialized = False

    def __init__(self):
        super(QueueView, self).__init__()

        self.queue_bar = list()

    def _initialize(self):
        QueueView._initialized = True

        self.add_property("SpriteProperty")
        self.add_property("BlitProperty")
        self.property("SpriteProperty").visible = True
        self.font = pygame.font.Font("assets/DisposableDroidBB.ttf", 16)
        self.property("SpriteProperty").surface = self.font.render("Turn Queue", True, [0, 0, 0])

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 1160
        self.position.y = 52

        # battle_logic = GameObject.get_object_pool().select_with_label('BattleLogic')[0]
        # character_model = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
        #
        # font = pygame.font.Font("assets/DisposableDroidBB.ttf", 16)
        # self.line = TextLine.get_instance()
        # self.line.set_font(font)
        # self.line.update(f'{battle_logic.current_character.name}')
        # self.attach_child(self.line)
        # self.line.property('SpriteProperty').visible = True
        # position = self.line.property('TransformProperty').position
        # position.y = 40
        # position.x = 0
        #
        # self.line_current_char = TextLine.get_instance()
        # self.line_current_char.set_font(font)
        # self.line_current_char.update(f'{battle_logic.current_character.name}')
        # self.attach_child(self.line_current_char)
        # self.line_current_char.property('SpriteProperty').visible = True
        # position = self.line_current_char.property('TransformProperty').position
        # position.y = 16
        # position.x = 0

        # Configure section description and TextLine for each character in queue
        self.font_16 = pygame.font.Font("assets/DisposableDroidBB.ttf", 16)

        step = 0
        battle_logic = GameObject.get_object_pool().select_with_label('BattleLogic')[0]
        for character in battle_logic.queue_view:
            line = TextLine.get_instance()
            line.set_font(self.font_16)
            line.property('SpriteProperty').visible = True

            position = line.property('TransformProperty').position
            position.y = 40
            position.y += step
            step += 30
            position.x = 0

            self.attach_child(line)
            self.queue_bar.append(line)

        for line in self.queue_bar:
            index = self.queue_bar.index(line)
            line.update(
                f'{battle_logic.queue_view[index].name}')

    def on_create(self):
        pass

    def on_script(self):
        if not QueueView._initialized and CharacterModel._initialized and len(GameObject.get_object_pool().select_with_label('CharacterModel')) != 0:
            self._initialize()
        else:
            pass

    def on_signal(self, signal):
        if signal.type == BattleLogic.CHARACTER_CHANGED_SIGNAL:
            # character_model = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
            battle_logic = GameObject.get_object_pool().select_with_label('BattleLogic')[0]
            # line = ''
            # self.line_current_char.update(f'Current Character: {battle_logic.current_character.name}')
            # for character in battle_logic.queue_view:
            #     line += character.name + ', '
            # self.line.update(f'Next: {line}')
            for line in self.queue_bar:
                index = self.queue_bar.index(line)
                line.update(
                    f'{battle_logic.queue_view[index].name}')
