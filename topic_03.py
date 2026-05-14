# ============================================================
# TOPIC 3: Arrays and Plotting
# NumPy arrays are faster and more powerful than Python lists
# for numerical data. numpy.array([...]) creates one from a
# list. Mathematical operations apply to every element at once.
# matplotlib.pyplot.plot() draws a line graph; plt.show()
# displays it in a window.
# ============================================================

from topic_02 import *
import numpy as np
import matplotlib.pyplot as plt

# 1D array — each index is a room. 0=empty, 1=enemy, 2=treasure
DUNGEON_ROOMS = np.array([0, 1, 0, 2, 1])


def plot_combat(hp_history, enemy_name="Enemy"):
    rounds = list(range(len(hp_history)))
    plt.figure(figsize=(6, 4))
    plt.plot(rounds, hp_history, marker="o", color="red")
    plt.title(f"{enemy_name} HP over Combat Rounds")
    plt.xlabel("Round")
    plt.ylabel("HP")
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    NAME = input("Enter your hero's name: ")
    display_stats(NAME, HP, ATTACK, GOLD)

    print(f"\nDungeon corridor: {DUNGEON_ROOMS}")
    print(f"Room legend — 0:empty  1:enemy  2:treasure")
    print(f"Enemy rooms:    {np.sum(DUNGEON_ROOMS == 1)}")
    print(f"Treasure rooms: {np.sum(DUNGEON_ROOMS == 2)}")

    # Simulate a short fight and plot enemy HP
    enemy_hp = 30
    hp_history = [enemy_hp]
    while enemy_hp > 0:
        dmg = calc_damage(ATTACK)
        enemy_hp = max(0, enemy_hp - dmg)
        hp_history.append(enemy_hp)

    print(f"\nDefeated enemy in {len(hp_history) - 1} rounds!")
    plot_combat(hp_history, "Goblin")
