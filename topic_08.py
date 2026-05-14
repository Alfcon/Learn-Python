# ============================================================
# TOPIC 8: Scripts and Automation
# argparse reads command-line flags so the user can configure
# the program without editing code. The if __name__ == "__main__"
# guard means a file only auto-runs when executed directly.
# Procedural generation uses an algorithm to create content
# (the dungeon) automatically.
# ============================================================

from topic_07 import *
import argparse


def generate_dungeon(size=7, difficulty="normal"):
    rng = np.random.default_rng(seed=42)
    grid = np.zeros((size, size), dtype=float)

    # Solid border of walls
    grid[1:-1, 1:-1] = 1  # interior is floor
    grid[0, :] = 0
    grid[-1, :] = 0
    grid[:, 0] = 0
    grid[:, -1] = 0

    enemy_counts = {"easy": 2, "normal": 4, "hard": 6}
    treasure_counts = {"easy": 3, "normal": 2, "hard": 1}
    n_enemies = enemy_counts.get(difficulty, 4)
    n_treasure = treasure_counts.get(difficulty, 2)

    centre = size // 2
    interior = [
        (r, c)
        for r in range(1, size - 1)
        for c in range(1, size - 1)
        if not (r == centre and c == centre)
    ]
    interior_arr = np.array(interior)
    rng.shuffle(interior_arr)

    for r, c in interior_arr[:n_enemies]:
        grid[r, c] = 2
    for r, c in interior_arr[n_enemies:n_enemies + n_treasure]:
        grid[r, c] = 3

    return grid


def parse_args():
    parser = argparse.ArgumentParser(description="Dungeon Adventure")
    parser.add_argument("--name", type=str, default=None,
                        help="Hero name (skips the prompt)")
    parser.add_argument("--difficulty", type=str, default="normal",
                        choices=["easy", "normal", "hard"],
                        help="Game difficulty")
    parser.add_argument("--size", type=int, default=7,
                        help="Dungeon grid size (default 7)")
    return parser.parse_args()


def main(args=None):
    if args is None:
        args = parse_args()

    dungeon = generate_dungeon(args.size, args.difficulty)
    centre = args.size // 2
    start_pos = [centre, centre]

    hero_name = args.name or input("Enter your hero's name: ").strip() or "Hero"
    hero = Hero(hero_name)
    hero.pos = start_pos

    print(f"\n  Difficulty: {args.difficulty.upper()}  |  Map: {args.size}x{args.size}")
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
                run_combat(hero, enemy)
                if not enemy.is_alive():
                    dungeon[hero.pos[0], hero.pos[1]] = 1
            else:
                print("  Nothing to attack here.")
        elif action == "pick" and len(cmd) > 2 and cmd[1] == "up":
            cell = int(dungeon[hero.pos[0], hero.pos[1]])
            if cell == 3:
                hero.pick_up(Item("Gold Coin", "shiny treasure", 10))
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
