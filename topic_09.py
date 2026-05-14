# ============================================================
# TOPIC 9: Quality and Testing
# unittest is Python's built-in testing framework. A test
# class inherits from unittest.TestCase. Each method starting
# with 'test_' is one test. assertEqual, assertTrue, assertFalse
# check that code behaves as expected. Run tests with:
#   python -m unittest topic_09
# ============================================================

from topic_08 import *
import unittest


class TestCalcDamage(unittest.TestCase):
    def test_minimum_damage(self):
        for _ in range(100):
            dmg = calc_damage(10)
            self.assertGreaterEqual(dmg, 11,
                "damage should be at least attack + 1")

    def test_maximum_damage(self):
        for _ in range(100):
            dmg = calc_damage(10)
            self.assertLessEqual(dmg, 16,
                "damage should be at most attack + 6")


class TestMove(unittest.TestCase):
    def setUp(self):
        self.open_grid = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ], dtype=float)

    def test_move_north_valid(self):
        result = move("north", [2, 2], self.open_grid)
        self.assertEqual(result, [1, 2])

    def test_move_into_wall_stays_put(self):
        result = move("north", [1, 2], self.open_grid)
        self.assertEqual(result, [1, 2])

    def test_unknown_direction_stays_put(self):
        result = move("diagonal", [2, 2], self.open_grid)
        self.assertEqual(result, [2, 2])


class TestInventoryFunctions(unittest.TestCase):
    def test_add_item_appends(self):
        inv = []
        add_item(inv, "Sword")
        self.assertIn("Sword", inv)

    def test_remove_item_deletes(self):
        inv = ["Sword", "Shield"]
        remove_item(inv, "Sword")
        self.assertNotIn("Sword", inv)
        self.assertIn("Shield", inv)

    def test_remove_missing_item_does_not_raise(self):
        inv = ["Shield"]
        remove_item(inv, "Potion")
        self.assertEqual(inv, ["Shield"])


class TestHero(unittest.TestCase):
    def test_initial_hp(self):
        hero = Hero("Tester")
        self.assertEqual(hero.hp, 100)

    def test_take_damage_reduces_hp(self):
        hero = Hero("Tester")
        hero.take_damage(30)
        self.assertEqual(hero.hp, 70)

    def test_hp_floor_is_zero(self):
        hero = Hero("Tester")
        hero.take_damage(9999)
        self.assertEqual(hero.hp, 0)

    def test_is_alive_false_when_dead(self):
        hero = Hero("Tester")
        hero.take_damage(100)
        self.assertFalse(hero.is_alive())


class TestEnemySubclasses(unittest.TestCase):
    def test_goblin_name(self):
        self.assertEqual(Goblin().name, "Goblin")

    def test_dragon_has_more_hp_than_goblin(self):
        self.assertGreater(Dragon().hp, Goblin().hp)

    def test_enemy_hp_floor_is_zero(self):
        g = Goblin()
        g.take_damage(9999)
        self.assertEqual(g.hp, 0)


class TestGenerateDungeon(unittest.TestCase):
    def test_shape(self):
        grid = generate_dungeon(size=7)
        self.assertEqual(grid.shape, (7, 7))

    def test_border_walls(self):
        grid = generate_dungeon(size=7)
        self.assertTrue(np.all(grid[0, :] == 0))
        self.assertTrue(np.all(grid[-1, :] == 0))
        self.assertTrue(np.all(grid[:, 0] == 0))
        self.assertTrue(np.all(grid[:, -1] == 0))

    def test_centre_is_floor(self):
        grid = generate_dungeon(size=7)
        self.assertEqual(int(grid[3, 3]), 1)


# ============================================================
# DEMO — runs the game; use python -m unittest topic_09 for tests
# ============================================================
if __name__ == "__main__":
    main()
