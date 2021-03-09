from action_types import ActionType
from card_manager import CardManager
from character_manager import CharacterManager
from item_manager import ItemManager
from process import Process

CardManager.load_config('card_types.json')
CharacterManager.load_config('character_types.json')
ItemManager.load_config('item_types.json')

player = CharacterManager.create_character("character_edward")
goblin = CharacterManager.create_character("character_goblin")

item1 = ItemManager.create_item('Short sword')
item2 = ItemManager.create_item('Simple shield')

player.add_item(item1)
player.add_item(item2)
print(player.inventory)
print(player.equipment)

player.add_equip('hand_r', item1)
player.add_equip('hand_l', item2)

print(player.equipment)


card1 = CardManager.create_card("Heavy Strike")
card2 = CardManager.create_card("Fast Strike")
card3 = CardManager.create_card("Piercing Strike")
card4 = CardManager.create_card("Nimble Strike")
card5 = CardManager.create_card("Magic Strike")
card6 = CardManager.create_card("Arcana Shot")
card7 = CardManager.create_card("Bow Shot")
card8 = CardManager.create_card("Shadow Dagger")
card9 = CardManager.create_card("Shield Bash")


player.deck.card_pool.append(card1)
player.deck.card_pool.append(card1)
player.deck.card_pool.append(card2)
player.deck.card_pool.append(card2)
player.deck.card_pool.append(card2)
player.deck.card_pool.append(card3)
player.deck.card_pool.append(card4)
player.deck.card_pool.append(card5)
player.deck.card_pool.append(card6)
player.deck.card_pool.append(card7)
player.deck.card_pool.append(card8)
player.deck.card_pool.append(card9)
print(f'Ilość kart w pool: {len(player.deck.card_pool)}')
print(f'Ilość kart w deck: {len(player.deck)}')

player.deck.add_card(card1)
player.deck.add_card(card1)
player.deck.add_card(card2)
player.deck.add_card(card2)
player.deck.add_card(card2)
player.deck.add_card(card3)
player.deck.add_card(card9)
print(f'Ilość kart w pool: {len(player.deck.card_pool)}')
print(f'Ilość kart w deck: {len(player.deck)}')

def get_hand(player):
    return player.deck

hand = get_hand(player)

# selected_card = hand[0]

# print(goblin.name.title() + " ma " + str(goblin.attributes.health) + " punktów życia.")
# Process.action_process(player, goblin, selected_card)
# print(player.name.title() + " trafia " + goblin.name.title() + " swoim " + selected_card.card_name + " za "
#       + str(selected_card.ap_cost) + "AP, zadając " + str(ActionType.dmg) + " obrażeń, zostaje mu "
#       + str(goblin.attributes.health) + " punktów życia.")
# Process.kill_character(goblin)
#
#
# selected_card = hand[1]
#
# print(goblin.name.title() + " ma " + str(goblin.attributes.health) + " punktów życia.")
# Process.action_process(player, goblin, selected_card)
# print(player.name.title() + " trafia " + goblin.name.title() + " swoim " + selected_card.card_name + " za "
#       + str(selected_card.ap_cost) + "AP, zadając " + str(ActionType.dmg) + " obrażeń, zostaje mu "
#       + str(goblin.attributes.health) + " punktów życia.")
# Process.kill_character(goblin)
#
# selected_card = hand[3]
#
# print(goblin.name.title() + " ma " + str(goblin.attributes.health) + " punktów życia.")
# Process.action_process(player, goblin, selected_card)
# print(player.name.title() + " trafia " + goblin.name.title() + " swoim " + selected_card.card_name + " za "
#       + str(selected_card.ap_cost) + "AP, zadając " + str(ActionType.dmg) + " obrażeń, zostaje mu "
#       + str(goblin.attributes.health) + " punktów życia.")
# Process.kill_character(goblin)

selected_card = hand[-1]

print(goblin.name.title() + " ma " + str(goblin.attributes.health) + " punktów życia.")
Process.action_process(player, goblin, selected_card)
print(player.name.title() + " trafia " + goblin.name.title() + " swoim " + selected_card.card_name + " za "
      + str(selected_card.ap_cost) + "AP, zadając " + str(ActionType.dmg) + " obrażeń, zostaje mu "
      + str(goblin.attributes.health) + " punktów życia.")
print(goblin.status)
Process.end_turn(goblin)
print(goblin.name.title() + " ma " + str(goblin.attributes.health) + " punktów życia.")
print(goblin.status)
print(f' {goblin.attributes.health}, {goblin.attributes.action_points}')
Process.end_turn(goblin)
print(goblin.status)
print(f' {goblin.attributes.health}, {goblin.attributes.action_points}')