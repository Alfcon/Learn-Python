# ============================================================
# TOPIC 5: Files and Grids
# open(filename, mode) opens a file: 'r' reads, 'w' writes.
# The 'with' statement closes the file automatically when the
# block exits. Reading a dungeon layout from a text file means
# the map can be edited without touching the code.
# ============================================================

from topic_04 import *
import os

SAVE_FILE = "save_game.txt"
MAP_FILE = "dungeon_map.txt"


def save_game(filename, hero_name, hero_hp, hero_gold, inventory, pos):
    with open(filename, "w") as f:
        f.write(f"{hero_name}\n")
        f.write(f"{hero_hp}\n")
        f.write(f"{hero_gold}\n")
        f.write(",".join(inventory) + "\n")
        f.write(f"{pos[0]},{pos[1]}\n")
    print(f"  Game saved to {filename}.")


def load_game(filename):
    if not os.path.exists(filename):
        print("  No save file found.")
        return None
    with open(filename, "r") as f:
        lines = f.read().splitlines()
    hero_name = lines[0]
    hero_hp = int(lines[1])
    hero_gold = int(lines[2])
    inventory = lines[3].split(",") if lines[3] else []
    pos = [int(x) for x in lines[4].split(",")]
    print(f"  Game loaded from {filename}.")
    return {"name": hero_name, "hp": hero_hp, "gold": hero_gold,
            "inventory": inventory, "pos": pos}


def load_dungeon_from_file(filename):
    grid = []
    with open(filename, "r") as f:
        for line in f:
            row = [int(c) for c in line.strip().split()]
            grid.append(row)
    return np.array(grid, dtype=float)


def write_default_map(filename):
    default = (
        "0 0 0 0 0\n"
        "0 1 2 1 0\n"
        "0 1 1 1 0\n"
        "0 1 3 2 0\n"
        "0 0 0 0 0\n"
    )
    with open(filename, "w") as f:
        f.write(default)


def main():
    if not os.path.exists(MAP_FILE):
        write_default_map(MAP_FILE)
    dungeon = load_dungeon_from_file(MAP_FILE)

    saved = load_game(SAVE_FILE)
    if saved:
        hero_name = saved["name"]
        hero_hp = saved["hp"]
        hero_gold = saved["gold"]
        hero_inv = saved["inventory"]
        pos = saved["pos"]
        print(f"  Welcome back, {hero_name}!")
    else:
        hero_name = input("Enter your hero's name: ")
        hero_hp = HP
        hero_gold = GOLD
        hero_inv = list(INVENTORY)
        pos = list(HERO_START)

    display_map(dungeon, pos)

    while True:
        cmd = input("\n> ").strip().lower().split()
        if not cmd:
            continue
        action = cmd[0]

        if action == "move" and len(cmd) > 1:
            pos = move(cmd[1], pos, dungeon)
            display_map(dungeon, pos)
        elif action == "attack":
            cell = int(dungeon[pos[0], pos[1]])
            if cell == 2:
                result = combat(hero_hp, ATTACK, 20)
                hero_hp = result["hero_hp"]
                plot_combat(result["hp_history"])
                if result["enemy_hp"] == 0:
                    dungeon[pos[0], pos[1]] = 1
                    hero_gold += 10
            else:
                print("  Nothing to attack here.")
        elif action == "save":
            save_game(SAVE_FILE, hero_name, hero_hp, hero_gold, hero_inv, pos)
        elif action == "load":
            saved = load_game(SAVE_FILE)
            if saved:
                hero_name = saved["name"]
                hero_hp = saved["hp"]
                hero_gold = saved["gold"]
                hero_inv = saved["inventory"]
                pos = saved["pos"]
        elif action == "stats":
            display_stats(hero_name, hero_hp, ATTACK, hero_gold)
            show_inventory(hero_inv)
        elif action == "quit":
            print(f"  Farewell, {hero_name}!")
            break
        else:
            print("  Commands: move <dir>  attack  save  load  stats  quit")

        if hero_hp <= 0:
            print("  You have died. Game over.")
            break


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    main()
