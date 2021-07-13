import pygame

from game_object.game_object import GameObject
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.text_line import TextLine
from assets.lib.battle_system.battle_logic import BattleLogic


class EnemyView(GameObject):

    _initialized = False

    def __init__(self):
        super(EnemyView, self).__init__()

        self.enemies_status = list()

    def _initialize(self):
        EnemyView._initialized = True
        print("PartyVIew initialized")

        self.enemies = GameObject.get_object_pool().select_with_label('CharacterModel')[0].enemies

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
        for character in self.enemies.take():
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
                f'{self.enemies.take()[index].name} - HP:{self.enemies.take()[index].attributes.health} AP:{self.enemies.take()[index].attributes.action_points}')

    def on_create(self):
        pass

    def on_script(self):
        if not EnemyView._initialized and CharacterModel._initialized:
            self._initialize()
        else:
            pass

        if EnemyView._initialized:
            pass

    def on_signal(self, signal):
        if EnemyView._initialized:
            if signal.type == BattleLogic.STATUS_RESET_SIGNAL:
                self.setup_party()
            if signal.type == BattleLogic.STATUS_UPDATE_SIGNAL:
                for line in self.enemies_status:
                    index = self.enemies_status.index(line)
                    line.update(f'{self.enemies.take()[index].name} - HP:{self.enemies.take()[index].attributes.health} AP:{self.enemies.take()[index].attributes.action_points}')
