from action_types import ActionType
from battle_logic import BattleLogic
from card_manager import CardManager
from character_manager import CharacterManager
from item_manager import ItemManager
from process import Process

CardManager.load_config('card_types.json')
CharacterManager.load_config('character_types.json')
ItemManager.load_config('item_types.json')

player = CharacterManager.create_character("character_edward")
goblin = CharacterManager.create_character("character_goblin")

player.inventory.add_item('Short sword')
player.inventory.add_item('Simple shield')
player.inventory.add_item('Simple shield')
player.inventory.add_item('Short sword')
player.inventory.add_item('Simple shield')
print(f'\nParametry startowe:')
print(f'deck: {player.deck}')
print(f'card_pool: {player.card_pool}')
print(f'inventory: {player.inventory}')
print(f'equipment: {player.equipment}')
print('\n')
player.add_equip('hand_r', 'Short sword')
print(f'deck: {player.deck}')
print(f'card_pool: {player.card_pool}')
print(f'inventory: {player.inventory}')
print(f'equipment: {player.equipment}')
print('\n')
player.add_equip('hand_l', 'Simple shield')
print(f'deck: {player.deck}')
print(f'card_pool: {player.card_pool}')
print(f'inventory: {player.inventory}')
print(f'equipment: {player.equipment}')
print('\n')
player.remove_equip('hand_l')
print(f'deck: {player.deck}')
print(f'card_pool: {player.card_pool}')
print(f'inventory: {player.inventory}')
print(f'equipment: {player.equipment}')
print('\n')
player.remove_equip('hand_r')
print(f'deck: {player.deck}')
print(f'card_pool: {player.card_pool}')
print(f'inventory: {player.inventory}')
print(f'equipment: {player.equipment}')
print(f'card_pool: {player.card_pool}')

player.inventory.remove_item('Simple shield')
print(f'inventory: {player.inventory}')

# BattleLogic.create_battledeck(player)
# print(player.battledeck)
#
# BattleLogic.get_hand(player, 3)
# print(player.hand)

# def get_hand(player):
#     return player.deck
#
# hand = get_hand(player)
#
#
# selected_card = hand[-1]
#
# print(goblin.name.title() + " ma " + str(goblin.attributes.health) + " punktów życia.")
# Process.action_process(player, goblin, selected_card)
# print(player.name.title() + " trafia " + goblin.name.title() + " swoim " + selected_card.card_name + " za "
#       + str(selected_card.ap_cost) + "AP, zadając " + str(ActionType.dmg) + " obrażeń, zostaje mu "
#       + str(goblin.attributes.health) + " punktów życia.")
# print(goblin.status)
# Process.end_turn(goblin)
# print(goblin.name.title() + " ma " + str(goblin.attributes.health) + " punktów życia.")
# print(goblin.status)
# print(f' {goblin.attributes.health}, {goblin.attributes.action_points}')
# Process.end_turn(goblin)
# print(goblin.status)
# print(f' {goblin.attributes.health}, {goblin.attributes.action_points}')