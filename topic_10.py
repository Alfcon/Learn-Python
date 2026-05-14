# ============================================================
# TOPIC 10: Data Processing and Analytics
# pandas stores tabular data in a DataFrame. Build one from a
# list of dicts: pd.DataFrame([{...}, {...}]). Methods like
# .mean(), .value_counts(), and .groupby() compute summaries.
# Use matplotlib to turn DataFrames into charts.
# ============================================================

from topic_09 import *
import pandas as pd

BATTLE_LOG = []


def log_battle(hero_name, enemy_name, damage_dealt, hero_survived):
    BATTLE_LOG.append({
        "hero":          hero_name,
        "enemy":         enemy_name,
        "damage_dealt":  damage_dealt,
        "survived":      hero_survived,
    })


def analyse_battles(log):
    if not log:
        print("  No battles recorded yet.")
        return None
    df = pd.DataFrame(log)
    print("\n  --- Battle Analytics ---")
    print(f"  Total battles : {len(df)}")
    print(f"  Win rate      : {df['survived'].mean() * 100:.1f}%")
    print(f"  Avg damage    : {df['damage_dealt'].mean():.1f}")
    counts = df['enemy'].value_counts().to_string()
    print(f"\n  Enemies faced:\n{counts}")
    return df


def plot_analytics(df):
    if df is None or df.empty:
        return
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    df.groupby("enemy")["damage_dealt"].mean().plot(
        kind="bar", ax=axes[0], color="steelblue"
    )
    axes[0].set_title("Avg Damage Dealt by Enemy Type")
    axes[0].set_xlabel("Enemy")
    axes[0].set_ylabel("Avg Damage")
    axes[0].tick_params(axis="x", rotation=0)

    outcomes = df["survived"].value_counts()
    labels = ["Survived" if k else "Died" for k in outcomes.index]
    axes[1].pie(outcomes.values, labels=labels, autopct="%1.0f%%",
                colors=["#4caf50", "#f44336"])
    axes[1].set_title("Battle Outcomes")

    plt.tight_layout()
    plt.show()


def run_combat_logged(hero, enemy):
    start_hp = enemy.hp
    hp_history = run_combat(hero, enemy)
    damage_dealt = start_hp - enemy.hp
    log_battle(hero.name, enemy.name, damage_dealt, hero.is_alive())
    return hp_history


def main(args=None):
    if args is None:
        args = parse_args()

    dungeon = generate_dungeon(args.size, args.difficulty)
    centre = args.size // 2
    hero_name = args.name or input("Enter your hero's name: ").strip() or "Hero"
    hero = Hero(hero_name)
    hero.pos = [centre, centre]

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
            break
        else:
            print("  Commands: move <dir>  attack  pick up  look  analytics  save  load  stats  quit")

        if not hero.is_alive():
            print("  You have died. Game over.")
            df = analyse_battles(BATTLE_LOG)
            plot_analytics(df)
            break


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    main()
