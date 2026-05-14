# ============================================================
# TOPIC 11: Engineering and Science Applications
# BFS (Breadth-First Search) explores a grid layer by layer
# to find the shortest path between two points. A heatmap
# visualises a 2D array as colour intensities — here it shows
# which rooms you have visited most. Procedural generation
# (introduced in topic_08) is extended to a random-walk dungeon.
# ============================================================

from topic_10 import *
from collections import deque

EXPLORED = None  # 2D array tracking visit counts, initialised in main()


def bfs_pathfind(grid, start, goal):
    rows, cols = grid.shape
    visited = {tuple(start)}
    queue = deque([(list(start), [list(start)])])
    while queue:
        pos, path = queue.popleft()
        if pos == list(goal):
            return path
        r, c = pos
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            nxt = [nr, nc]
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr, nc] != 0
                    and tuple(nxt) not in visited):
                visited.add(tuple(nxt))
                queue.append((nxt, path + [nxt]))
    return []


def generate_dungeon_procedural(size=11, seed=None):
    rng = np.random.default_rng(seed)
    grid = np.zeros((size, size), dtype=float)

    # Random walk from centre to carve floor tiles
    r, c = size // 2, size // 2
    grid[r, c] = 1
    for _ in range(size * size * 3):
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if 1 <= nr < size - 1 and 1 <= nc < size - 1:
            grid[nr, nc] = 1
            r, c = nr, nc

    # Place enemies and treasure on floor tiles away from start
    floor_cells = [
        (fr, fc)
        for fr in range(size)
        for fc in range(size)
        if grid[fr, fc] == 1 and not (fr == size // 2 and fc == size // 2)
    ]
    rng.shuffle(floor_cells)
    for fr, fc in floor_cells[:4]:
        grid[fr, fc] = 2
    for fr, fc in floor_cells[4:7]:
        grid[fr, fc] = 3

    return grid


def find_nearest_enemy(grid, pos):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:
                path = bfs_pathfind(grid, pos, [r, c])
                if path:
                    return [r, c], path
    return None, []


def plot_heatmap(explored, title="Rooms Explored"):
    plt.figure(figsize=(5, 5))
    plt.imshow(explored, cmap="YlOrRd", interpolation="nearest")
    plt.colorbar(label="Times visited")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def main(args=None):
    global EXPLORED

    if args is None:
        args = parse_args()

    dungeon = generate_dungeon_procedural(seed=42)
    size = dungeon.shape[0]
    centre = size // 2
    start_pos = [centre, centre]

    EXPLORED = np.zeros_like(dungeon, dtype=float)

    hero_name = args.name or input("Enter your hero's name: ").strip() or "Hero"
    hero = Hero(hero_name)
    hero.pos = start_pos
    EXPLORED[start_pos[0], start_pos[1]] += 1

    print(f"\n  Procedurally generated dungeon ({size}x{size})")
    display_map(dungeon, hero.pos)

    while True:
        cmd = safe_input("\n> ").split()
        if not cmd:
            continue
        action = cmd[0]

        if action == "move" and len(cmd) > 1:
            hero.pos = move(cmd[1], hero.pos, dungeon)
            EXPLORED[hero.pos[0], hero.pos[1]] += 1
            display_map(dungeon, hero.pos)
        elif action == "attack":
            cell = int(dungeon[hero.pos[0], hero.pos[1]])
            if cell == 2:
                enemy = get_enemy_for_cell(cell)
                run_combat_logged(hero, enemy)
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
        elif action == "pathfind":
            goal, path = find_nearest_enemy(dungeon, hero.pos)
            if path:
                print(f"  Nearest enemy at {goal}. Path length: {len(path) - 1} steps.")
                print(f"  Next step: {path[1] if len(path) > 1 else goal}")
            else:
                print("  No enemies reachable.")
        elif action == "heatmap":
            plot_heatmap(EXPLORED)
        elif action == "analytics":
            df = analyse_battles(BATTLE_LOG)
            plot_analytics(df)
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
            df = analyse_battles(BATTLE_LOG)
            plot_analytics(df)
            plot_heatmap(EXPLORED)
            break
        else:
            print("  Commands: move <dir>  attack  pick up  look  pathfind  heatmap  analytics  save  load  stats  quit")

        if not hero.is_alive():
            print("  You have died. Game over.")
            df = analyse_battles(BATTLE_LOG)
            plot_analytics(df)
            plot_heatmap(EXPLORED)
            break


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    main()
