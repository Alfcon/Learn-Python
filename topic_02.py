# ============================================================
# TOPIC 2: Strings and Lists
# Strings are sequences of characters. f-strings embed
# variables: f"Hello {name}". Methods like .upper() and
# .split() transform them. Lists are ordered, mutable
# collections. .append() adds items, .remove() deletes them,
# and 'in' tests membership.
# ============================================================

from topic_01 import *

INVENTORY = []
ROOM_NAMES = [
    "The Dark Corridor",
    "The Goblin's Lair",
    "The Dragon's Den",
    "The Treasure Vault",
]


def add_item(inventory, item_name):
    inventory.append(item_name)
    print(f"  + Picked up: {item_name}")


def remove_item(inventory, item_name):
    if item_name in inventory:
        inventory.remove(item_name)
        print(f"  - Used: {item_name}")
    else:
        print(f"  ! You don't have: {item_name}")


def show_inventory(inventory):
    if inventory:
        print("Inventory: " + ", ".join(inventory))
    else:
        print("Inventory: (empty)")


def describe_room(room_name):
    return f"You enter {room_name.upper()}. Shadows press in around you."


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    NAME = input("Enter your hero's name: ")
    display_stats(NAME, HP, ATTACK, GOLD)
    print(describe_room(ROOM_NAMES[0]))
    add_item(INVENTORY, "Sword")
    add_item(INVENTORY, "Health Potion")
    show_inventory(INVENTORY)
    remove_item(INVENTORY, "Health Potion")
    show_inventory(INVENTORY)
    print(f"\nRoom count: {len(ROOM_NAMES)}")
    print(f"First room uppercase: {ROOM_NAMES[0].upper()}")
