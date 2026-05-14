# ============================================================
# TOPIC 6: Modelling the World with Objects
# A class is a blueprint for objects. __init__ is the
# constructor — it runs when you create an instance.
# self refers to the specific object being acted on.
# Methods are functions belonging to a class.
# Hero, Enemy, and Item replace the loose variables used before.
# ============================================================

from topic_05 import *


class Item:
    def __init__(self, name, description, value=0):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return f"{self.name} ({self.description}, worth {self.value}g)"


class Enemy:
    def __init__(self, name, hp, attack, gold_drop):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.gold_drop = gold_drop

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)


class Hero:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack = 10
        self.gold = 0
        self.inventory = []
        self.pos = list(HERO_START)

    def attack_enemy(self, enemy):
        dmg = calc_damage(self.attack)
        enemy.take_damage(dmg)
        print(f"  {self.name} hits {enemy.name} for {dmg}! ({enemy.name} HP: {enemy.hp})")
        return dmg

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def is_alive(self):
        return self.hp > 0

    def pick_up(self, item):
        self.inventory.append(item)
        print(f"  + Picked up: {item.name}")

    def display_stats(self):
        display_stats(self.name, self.hp, self.attack, self.gold)
        show_inventory([i.name for i in self.inventory])

    def save(self, filename=None):
        fname = filename or SAVE_FILE
        inv_names = [i.name for i in self.inventory]
        save_game(fname, self.name, self.hp, self.gold, inv_names, self.pos)

    def load(self, filename=None):
        fname = filename or SAVE_FILE
        data = load_game(fname)
        if data:
            self.name = data["name"]
            self.hp = data["hp"]
            self.gold = data["gold"]
            self.pos = data["pos"]
            self.inventory = [Item(n, "") for n in data["inventory"]]


def run_combat(hero, enemy):
    hp_history = [enemy.hp]
    while hero.is_alive() and enemy.is_alive():
        hero.attack_enemy(enemy)
        hp_history.append(enemy.hp)
        if enemy.is_alive():
            dmg = calc_damage(enemy.attack)
            hero.take_damage(dmg)
            print(f"  {enemy.name} hits back for {dmg}! (Your HP: {hero.hp})")
    if not enemy.is_alive():
        hero.gold += enemy.gold_drop
        print(f"  Victory! Gained {enemy.gold_drop} gold.")
    else:
        print("  You were defeated...")
    plot_combat(hp_history, enemy.name)
    return hp_history


def main():
    if not os.path.exists(MAP_FILE):
        write_default_map(MAP_FILE)
    dungeon = load_dungeon_from_file(MAP_FILE)

    hero = Hero(input("Enter your hero's name: "))
    display_map(dungeon, hero.pos)

    while True:
        cmd = input("\n> ").strip().lower().split()
        if not cmd:
            continue
        action = cmd[0]

        if action == "move" and len(cmd) > 1:
            hero.pos = move(cmd[1], hero.pos, dungeon)
            display_map(dungeon, hero.pos)
        elif action == "attack":
            cell = int(dungeon[hero.pos[0], hero.pos[1]])
            if cell == 2:
                enemy = Enemy("Dungeon Crawler", 20, 5, 10)
                run_combat(hero, enemy)
                if not enemy.is_alive():
                    dungeon[hero.pos[0], hero.pos[1]] = 1
            else:
                print("  Nothing to attack here.")
        elif action == "pick" and len(cmd) > 2 and cmd[1] == "up":
            cell = int(dungeon[hero.pos[0], hero.pos[1]])
            if cell == 3:
                item = Item("Gold Coin", "shiny treasure", 10)
                hero.pick_up(item)
                dungeon[hero.pos[0], hero.pos[1]] = 1
            else:
                print("  Nothing to pick up here.")
        elif action == "save":
            hero.save()
        elif action == "load":
            hero.load()
        elif action == "stats":
            hero.display_stats()
        elif action == "quit":
            print(f"  Farewell, {hero.name}!")
            break
        else:
            print("  Commands: move <dir>  attack  pick up  save  load  stats  quit")

        if not hero.is_alive():
            print("  You have died. Game over.")
            break


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    main()
