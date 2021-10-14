import pygame

from game_object.game_object import GameObject
from assets.lib.battle_system.controllers.character_controller import CharacterController
from assets.lib.ui.base_ui.text_line import TextLine


class EnemyView(GameObject):

    # EnamyView SharedResources definitions

    @property
    def enemies(self):
        return self._enemies.take()

    @enemies.setter
    def enemies(self, enemies):
        self._enemies.set(enemies)

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(EnemyView, self).__init__()

        self.enemies_status = list()

    def _initialize(self):
        EnemyView._initialized = True
        print("PartyVIew initialized")

        self._enemies = GameObject.get_object_pool().select_with_label('CharacterController')[0]._battle_enemies

        # TODO: Do przygotowania Properties/Components ręcznie tworzonych dla klas powinna być jakaś metoda prepare,
        #  on_create albo construct
        self.add_property("SpriteProperty")
        self.add_property("BlitProperty")
        self.property("SpriteProperty").visible = True
        self.font_24 = pygame.font.Font("assets/DisposableDroidBB.ttf", 24)
        self.property("SpriteProperty").surface = self.font_24.render("Enemies", True, [0, 0, 0])

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 1040
        self.position.y = 380

        # Configure section description and TextLine for each character in ally
        self.font_18 = pygame.font.Font("assets/DisposableDroidBB.ttf", 18)

        # self.setup_party()

    def setup_party(self):
        step = 0
        for character in self.enemies:
            line = TextLine.get_instance()
            line.set_font(self.font_18)
            line.property('SpriteProperty').visible = True

            position = line.property('TransformProperty').position
            position.y = 40
            position.y += step
            step += 60
            position.x = 0

            self.attach_child(line)
            self.enemies_status.append(line)

        for line in self.enemies_status:
            index = self.enemies_status.index(line)
            line.update(
                f'{self.enemies[index].name} - HP:{self.enemies[index].base_attributes.health} AP:{self.enemies[index].base_attributes.action_points}')

    def on_create(self):
        pass

    def on_script(self):
        if not EnemyView._initialized and CharacterController._initialized:
            self._initialize()
        else:
            pass

        if EnemyView._initialized:
            pass

    def on_signal(self, signal):
        if EnemyView._initialized:
            pass