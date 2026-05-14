# ============================================================
# TOPIC 4: 2D Arrays and Functions
# A 2D NumPy array (matrix) is a grid indexed by [row, col].
# numpy.zeros((rows, cols)) creates a grid of zeros.
# Functions package reusable logic: def name(params): body.
# return sends a value back to the caller. The game loop
# starts here — the player types commands each turn.
# ============================================================

from topic_03 import *

# 5x5 grid — 0:wall  1:floor  2:enemy  3:treasure
DUNGEON_GRID = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 2, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 3, 2, 0],
    [0, 0, 0, 0, 0],
])

HERO_START = [2, 2]

DIRECTION_MAP = {
    "north": (-1, 0),
    "south": (1, 0),
    "west":  (0, -1),
    "east":  (0, 1),
}


def move(direction, pos, grid):
    if direction not in DIRECTION_MAP:
        print("  Unknown direction. Try: north, south, east, west")
        return pos
    dr, dc = DIRECTION_MAP[direction]
    new_r, new_c = pos[0] + dr, pos[1] + dc
    if new_r < 0 or new_r >= grid.shape[0] or new_c < 0 or new_c >= grid.shape[1]:
        print("  A wall blocks your path.")
        return pos
    if grid[new_r, new_c] == 0:
        print("  A wall blocks your path.")
        return pos
    print(f"  Moved {direction}.")
    return [new_r, new_c]


def combat(hero_hp, hero_attack, enemy_hp, enemy_attack=5):
    hp_history = [enemy_hp]
    rounds = 0
    while hero_hp > 0 and enemy_hp > 0:
        dmg = calc_damage(hero_attack)
        enemy_hp = max(0, enemy_hp - dmg)
        hp_history.append(enemy_hp)
        if enemy_hp > 0:
            hero_hp = max(0, hero_hp - enemy_attack)
        rounds += 1
    outcome = "Victory!" if enemy_hp == 0 else "Defeated..."
    print(f"  Combat over in {rounds} rounds. {outcome}")
    return {"hero_hp": hero_hp, "enemy_hp": enemy_hp, "hp_history": hp_history}


def display_map(grid, hero_pos):
    symbols = {0: "#", 1: ".", 2: "E", 3: "T"}
    print()
    for r in range(grid.shape[0]):
        row_str = ""
        for c in range(grid.shape[1]):
            if [r, c] == hero_pos:
                row_str += "@"
            else:
                row_str += symbols.get(int(grid[r, c]), "?")
        print(row_str)
    print("  # wall  . floor  E enemy  T treasure  @ you")


def main():
    hero_name = input("Enter your hero's name: ")
    hero_hp = HP
    hero_gold = GOLD
    hero_inv = list(INVENTORY)
    pos = list(HERO_START)
    dungeon = DUNGEON_GRID.copy().astype(float)

    print(f"\nWelcome, {hero_name}! Defeat enemies (E) and find treasure (T).")
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
        elif action == "stats":
            display_stats(hero_name, hero_hp, ATTACK, hero_gold)
            show_inventory(hero_inv)
        elif action == "quit":
            print(f"  Farewell, {hero_name}!")
            break
        else:
            print("  Commands: move <dir>  attack  stats  quit")

        if hero_hp <= 0:
            print("  You have died. Game over.")
            break


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    main()
