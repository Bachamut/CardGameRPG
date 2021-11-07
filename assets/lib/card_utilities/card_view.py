from asserts.type_assert import TypeAssert
from game_object.game_object import GameObject

from assets.lib.card_utilities.card_model import FullCard


class HandCardView(GameObject):

    def __init__(self, full_card_model):
        TypeAssert.equal(full_card_model, FullCard)
        super(HandCardView, self).__init__()

        self.object_class = 'HandCardView'
        self.object_label = full_card_model.card_type
        self.object_type = 'CardView'

        # Set reference to model
        self._model = full_card_model

        # Add Object Properties
        self.add_property('TransformProperty')
        self.add_property('SpriteProperty')
        self.add_property('BlitProperty')

        # Configure Object Properties
        config = {'package': 'card_assets', 'set_resource': self._model.resource_name}
        self.property('SpriteProperty').configure(config)
