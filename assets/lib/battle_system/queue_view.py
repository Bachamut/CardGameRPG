import pygame

from game_object.game_object import GameObject
from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.battle_system.controllers.queue_controller import QueueController


class QueueView(GameObject):

    # QueueView SharedResources definitions

    @property
    def queue(self):
        return self._queue.take()

    @queue.setter
    def queue(self, enemies):
        self._queue.set(enemies)

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(QueueView, self).__init__()

        self.queue_bar = list()

    def _initialize(self):
        QueueView._initialized = True
        print("QueueView initialized")

        self._queue = GameObject.get_object_pool().select_with_label('QueueController')[0]._queue

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

        # InitializeProperty.started(self)
        self.property('InitializeProperty').property_disable()

    def on_create(self):
        pass

    def on_script(self):
        if not QueueView._initialized and QueueController._initialized:
            self._initialize()
        else:
            # var = self.queue
            pass

    def on_signal(self, signal):
        if QueueView._initialized:
            pass
