# ============================================================
# TOPIC 1: Introduction to Python
# Variables store data — numbers (int, float) and text (str).
# Expressions combine variables with operators to compute values.
# input() reads a line from the keyboard as a string.
# print() displays output. random.randint(a, b) returns a
# random integer between a and b inclusive.
# ============================================================

import random

NAME = "Hero"
HP = 100
ATTACK = 10
GOLD = 0


def calc_damage(attack):
    return attack + random.randint(1, 6)


def display_stats(name, hp, attack, gold):
    print(f"\n--- {name} ---")
    print(f"  HP:     {hp}")
    print(f"  Attack: {attack}")
    print(f"  Gold:   {gold}")


# ============================================================
# DEMO — run this file directly to see Topic 1 in action
# ============================================================
if __name__ == "__main__":
    NAME = input("Enter your hero's name: ")
    display_stats(NAME, HP, ATTACK, GOLD)
    dmg = calc_damage(ATTACK)
    print(f"\n{NAME} swings for {dmg} damage!")
