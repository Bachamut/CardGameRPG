import pygame

from game_object.game_object import GameObject
from assets.lib.text_line import TextLine
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.queue_model import QueueModel


class QueueView(GameObject):

    _initialized = False

    def __init__(self):
        super(QueueView, self).__init__()

        self.queue_bar = list()

    def _initialize(self):
        QueueView._initialized = True

        self.queue = GameObject.get_object_pool().select_with_label('QueueModel')[0].queue

        self.add_property("SpriteProperty")
        self.add_property("BlitProperty")
        self.property("SpriteProperty").visible = True
        self.font = pygame.font.Font("assets/DisposableDroidBB.ttf", 16)
        self.property("SpriteProperty").surface = self.font.render("Turn Queue", True, [0, 0, 0])

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 1160
        self.position.y = 52

        # Configure section description and TextLine for each character in queue
        self.font_16 = pygame.font.Font("assets/DisposableDroidBB.ttf", 16)

        step = 0
        for character in self.queue:
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
                f'{self.queue[index].name}')

    def on_create(self):
        pass

    def on_script(self):
        if not QueueView._initialized and QueueModel._initialized:
            self._initialize()
        else:
            var = self.queue
            pass

    def on_signal(self, signal):
        if QueueView._initialized:
            if signal.type == BattleLogic.CURRENT_CHARACTER_SIGNAL:
                for line in self.queue_bar:
                    index = self.queue_bar.index(line)
                    line.update(
                        f'{self.queue[index].name}')
