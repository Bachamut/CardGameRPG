import pygame

from game_object.game_object import GameObject
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.text_line import TextLine
from assets.lib.battle_system.battle_logic import BattleLogic


class CharacterIcon(GameObject):

    def __init__(self):
        super(CharacterIcon, self).__init__()
        self.object_class = 'CharacterIcon'

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.add_property('SpriteProperty')
        self.property('SpriteProperty').set_resource('CharacterIcon')
        self.add_property('BlitProperty')


class CharacterName(TextLine):

    def __init__(self, character_name):
        super(CharacterName, self).__init__()
        self.object_class = 'CharacterName'

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.add_property('SpriteProperty')
        self.property('SpriteProperty').set_resource('CharacterIcon')
        self.add_property('BlitProperty')

        self.character_name = character_name

        self.font_20 = pygame.font.Font("assets/DisposableDroidBB.ttf", 20)
        self.set_font(self.font_20)
        self.update(self.character_name)


class AttributeLine(GameObject):

    def __init__(self, attribute, value):
        super(AttributeLine, self).__init__()
        self.object_class = 'AttributeLine'

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position

        self._attribute = attribute
        self._value = value

        self.font_20 = pygame.font.Font("assets/DisposableDroidBB.ttf", 20)

        self.attribute = TextLine.get_instance()
        self.value = TextLine.get_instance()

        self.attribute.set_font(self.font_20)
        self.value.set_font(self.font_20)

        self.attribute.update(self._attribute)
        self.value.update(str(self._value))

        self.attach_child(self.attribute)
        self.attach_child(self.value)

        position = self.attribute.property('TransformProperty').position
        position.x = 0
        position.y = 0

        position = self.value.property('TransformProperty').position
        position.x = 20
        position.y = 0

    def update(self):
        pass


class PartyCharacterView(GameObject):

    def __init__(self, character):
        super(PartyCharacterView, self).__init__()
        self.object_class = 'PartyCharacterView'

        self.character = character

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position

        self.character_icon = CharacterIcon()
        self.character_name = CharacterName(self.character.name)
        self.character_hp = AttributeLine("HP", self.character.attributes.health)
        self.character_ep = AttributeLine("EP", self.character.attributes.energy)

        self.attach_child(self.character_icon)
        self.attach_child(self.character_name)
        self.attach_child(self.character_hp)
        self.attach_child(self.character_ep)

        position = self.character_name.property('TransformProperty').position
        position.x = 68
        position.y = 4

        position = self.character_hp.property('TransformProperty').position
        position.x = 136
        position.y = 4

        position = self.character_ep.property('TransformProperty').position
        position.x = 196
        position.y = 4


class PartyView(GameObject):

    _initialized = False

    def __init__(self):
        super(PartyView, self).__init__()
        self.object_class = 'PartyView'

        self.characters_status = list()

    def _initialize(self):
        PartyView._initialized = True
        print("PartyVIew initialized")

        self.ally = GameObject.get_object_pool().select_with_label('CharacterModel')[0].ally

        # self.add_property("SpriteProperty")
        # self.add_property("BlitProperty")
        # self.property("SpriteProperty").visible = True
        self.font_24 = pygame.font.Font("assets/DisposableDroidBB.ttf", 24)
        # self.property("SpriteProperty").surface = self.font_24.render("Party", True, [0, 0, 0])

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 16
        self.position.y = 200

        # Configure section description and TextLine for each character in ally
        self.font_18 = pygame.font.Font("assets/DisposableDroidBB.ttf", 18)

        # self.setup_party()

    def setup_party(self):
        # title = TextLine.get_instance()
        # title.set_font(self.font_24)

        step = 0
        for character in self.ally:
            line = PartyCharacterView(character)

            position = line.property('TransformProperty').position
            position.y = 40
            position.y += step
            step += 60
            position.x = 0

            self.attach_child(line)
            self.characters_status.append(line)

        # for line in self.characters_status:
        #     index = self.characters_status.index(line)
        #     line.update(
        #         f'{self.ally[index].name} - HP:{self.ally[index].attributes.health} AP:{self.ally[index].attributes.action_points}')

    def on_create(self):
        pass

    def on_script(self):
        if not PartyView._initialized and CharacterModel._initialized:
            self._initialize()
        else:
            pass

        if PartyView._initialized:
            pass

    def on_signal(self, signal):
        if PartyView._initialized:
            if signal.type == BattleLogic.STATUS_RESET_SIGNAL:
                self.setup_party()
            if signal.type == BattleLogic.STATUS_UPDATE_SIGNAL:
                for line in self.characters_status:
                    index = self.characters_status.index(line)
                    line.update(f'{self.ally[index].name} - HP:{self.ally[index].attributes.health} AP:{self.ally[index].attributes.action_points}')
