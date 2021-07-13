import pygame

from game_object.game_object import GameObject
from assets.lib.text_line import TextLine


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

    def update(self):
        self.character_hp.update(self.character.attributes.health)
        self.character_ep.update(self.character.attributes.energy)

    def equal(self, character):
        if self.character == character:
            return True

        return False


class AttributeLine(GameObject):

    def __init__(self, attribute, value, color=(0, 0, 0)):
        super(AttributeLine, self).__init__()
        self.object_class = 'AttributeLine'

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position

        self._attribute = attribute
        self._value = value

        self.font_20 = pygame.font.Font("assets/DisposableDroidBB.ttf", 20)
        self.font_20_bold = pygame.font.Font("assets/DisposableDroidBB_bld.ttf", 20)

        self.attribute = TextLine.get_instance()
        self.value = TextLine.get_instance()

        self.attribute.set_font(self.font_20_bold)
        self.value.set_font(self.font_20)

        self.attribute.update(self._attribute, color)
        self.value.update(self._value, color)

        self.attach_child(self.attribute)
        self.attach_child(self.value)

        position = self.attribute.property('TransformProperty').position
        position.x = 0
        position.y = 0

        position = self.value.property('TransformProperty').position
        position.x = 22
        position.y = 0

    def update(self, value):
        self._value = value
        self.value.update(self._value)


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


class CharacterIcon(GameObject):

    def __init__(self):
        super(CharacterIcon, self).__init__()
        self.object_class = 'CharacterIcon'

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.add_property('SpriteProperty')
        self.property('SpriteProperty').set_resource('CharacterIcon')
        self.add_property('BlitProperty')