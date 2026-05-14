# ============================================================
# TOPIC 7: Object Relationships and Exception Handling
# Inheritance: class Goblin(Enemy) means Goblin is a specialised
# Enemy — it reuses Enemy's methods and can override them.
# super().__init__() calls the parent class constructor.
# try/except catches errors at runtime so the program handles
# them gracefully instead of crashing.
# ============================================================

from topic_06 import *
import random as _random


class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", hp=20, attack=5, gold_drop=10)


class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="Dragon", hp=80, attack=25, gold_drop=100)


class Room:
    def __init__(self, room_type, enemy=None, item=None):
        self.room_type = room_type
        self.enemy = enemy
        self.item = item

    def describe(self):
        descriptions = {
            0: "A solid wall.",
            1: "An empty room.",
            2: f"A room containing a {self.enemy.name}!" if self.enemy else "A room with a defeated enemy.",
            3: f"A room with {self.item.name}!" if self.item else "A room with an empty chest.",
        }
        return descriptions.get(self.room_type, "A mysterious room.")


def get_enemy_for_cell(_cell_value):
    return Dragon() if _random.random() < 0.2 else Goblin()


def safe_input(prompt):
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return "quit"


def main():
    if not os.path.exists(MAP_FILE):
        write_default_map(MAP_FILE)

    try:
        dungeon = load_dungeon_from_file(MAP_FILE)
    except (FileNotFoundError, ValueError):
        print("  Map file unreadable. Using default.")
        dungeon = DUNGEON_GRID.copy().astype(float)

    try:
        hero = Hero(input("Enter your hero's name: ").strip() or "Hero")
    except (EOFError, KeyboardInterrupt):
        hero = Hero("Hero")

    display_map(dungeon, hero.pos)

    while True:
        cmd = safe_input("\n> ").split()
        if not cmd:
            continue
        action = cmd[0]

        if action == "move" and len(cmd) > 1:
            hero.pos = move(cmd[1], hero.pos, dungeon)
            display_map(dungeon, hero.pos)
        elif action == "attack":
            cell = int(dungeon[hero.pos[0], hero.pos[1]])
            if cell == 2:
                enemy = get_enemy_for_cell(cell)
                room = Room(2, enemy=enemy)
                print(f"  {room.describe()}")
                run_combat(hero, enemy)
                if not enemy.is_alive():
                    dungeon[hero.pos[0], hero.pos[1]] = 1
            else:
                print("  Nothing to attack here.")
        elif action == "pick" and len(cmd) > 2 and cmd[1] == "up":
            cell = int(dungeon[hero.pos[0], hero.pos[1]])
            if cell == 3:
                item = Item("Gold Coin", "shiny treasure", 10)
                room = Room(3, item=item)
                print(f"  {room.describe()}")
                hero.pick_up(item)
                dungeon[hero.pos[0], hero.pos[1]] = 1
            else:
                print("  Nothing to pick up here.")
        elif action == "look":
            cell = int(dungeon[hero.pos[0], hero.pos[1]])
            enemy = get_enemy_for_cell(cell) if cell == 2 else None
            item = Item("Gold Coin", "shiny treasure", 10) if cell == 3 else None
            print(f"  {Room(cell, enemy=enemy, item=item).describe()}")
        elif action == "save":
            try:
                hero.save()
            except OSError as e:
                print(f"  Could not save: {e}")
        elif action == "load":
            try:
                hero.load()
            except (OSError, ValueError, IndexError) as e:
                print(f"  Could not load: {e}")
        elif action == "stats":
            hero.display_stats()
        elif action == "quit":
            print(f"  Farewell, {hero.name}!")
            break
        else:
            print("  Commands: move <dir>  attack  pick up  look  save  load  stats  quit")

        if not hero.is_alive():
            print("  You have died. Game over.")
            break


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    main()
