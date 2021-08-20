from game_object.game_object import GameObject


class CharacterView(GameObject):

    def __init__(self, battle_character):
        super(CharacterView, self).__init__()

        # reference to character
        self.character_model = battle_character.object_hash

    @staticmethod
    def create_character_view(battle_models):
        character_view_list = list()
        for battle_character in battle_models:
            view = CharacterView(battle_character)
            character_view_list.append(view)

        return character_view_list