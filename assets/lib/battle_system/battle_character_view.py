from game_object.game_object import GameObject

from assets.lib.battle_system.battle_logic import BattleLogic


class BattleCharacterView(GameObject):

    def __init__(self, battle_character):
        super(BattleCharacterView, self).__init__()

        self.add_property("SignalProperty")
        self.property("SignalProperty").property_enable()

        # reference to character
        self.character_model = battle_character
        self.character_model_hash = battle_character.object_hash

        print(f'name: {battle_character.name} hash: {battle_character.object_hash}')

    def on_signal(self, signal):

        if signal.type == BattleLogic.CHARACTER_VIEW_SIGNAL and signal.subtype == "TARGET":
            if signal.receiver.object_hash == self.character_model.object_hash:

                print(f'CHARACTER_VIEW_SIGNAL:TARGET processed on receiver')

                return


        if signal.type == BattleLogic.CHARACTER_VIEW_SIGNAL and signal.subtype == "CASTER":
            if signal.receiver.object_hash == self.character_model.object_hash:

                print(f'CHARACTER_VIEW_SIGNAL:CASTER processed on receiver')

                return
