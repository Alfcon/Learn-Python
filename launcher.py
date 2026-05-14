import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import os
import sys

try:
    from pygments import lex
    from pygments.lexers import Python3Lexer
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

TOPIC_LABELS = [
    "Topic 01 — Variables & I/O",
    "Topic 02 — Strings & Lists",
    "Topic 03 — Arrays & Plotting",
    "Topic 04 — 2D Arrays & Functions",
    "Topic 05 — Files & Grids",
    "Topic 06 — Classes & Objects",
    "Topic 07 — Inheritance & Exceptions",
    "Topic 08 — Scripts & argparse",
    "Topic 09 — Testing",
    "Topic 10 — pandas Analytics",
    "Topic 11 — Algorithms & Heatmaps",
]

TOPIC_FILES = [f"topic_{i:02d}.py" for i in range(1, 12)]

BG_DARK = "#1e1e1e"
FG_DEFAULT = "#d4d4d4"
FONT_CODE = ("Consolas", 10)
FONT_EXPLAIN = ("Segoe UI", 11)
FONT_LIST = ("Segoe UI", 11)

TOKEN_COLORS = {
    "Token.Keyword":            "#569cd6",
    "Token.Keyword.Namespace":  "#c586c0",
    "Token.Name.Builtin":       "#4ec9b0",
    "Token.Name.Function":      "#dcdcaa",
    "Token.Name.Class":         "#4ec9b0",
    "Token.String":             "#ce9178",
    "Token.String.Doc":         "#6a9955",
    "Token.Comment":            "#6a9955",
    "Token.Comment.Single":     "#6a9955",
    "Token.Literal.Number":     "#b5cea8",
    "Token.Operator":           "#d4d4d4",
    "Token.Punctuation":        "#d4d4d4",
    "Token.Name.Decorator":     "#dcdcaa",
    "Token.Error":              "#f44747",
}

EXPLANATIONS = {
    0: """Topic 01 — Variables & I/O

A variable is a named box that stores a value. Python lets you create one just by writing:

    name = "Hero"
    hp = 100

The type (text, number, etc.) is figured out automatically.

input() pauses the program and waits for the player to type something. print() displays text back to them. Everything the game needs to know about the hero starts here as plain variables.

New in this topic:
  • Variables: NAME, HP, ATTACK, GOLD
  • calc_damage() — adds a random dice roll to attack
  • display_stats() — prints all hero info neatly
  • Basic damage formula: damage = attack + random 1–6
""",
    1: """Topic 02 — Strings & Lists

A string is a piece of text. You can join strings with +, slice them with [start:end], and format them with f-strings:

    f"You enter {room_name.upper()}!"

A list is an ordered collection. Items can be added with .append() and removed with .remove():

    inventory = []
    inventory.append("Sword")

The game uses a list as the player's inventory, and formatted strings to describe rooms.

New in this topic:
  • INVENTORY list
  • ROOM_NAMES — four named rooms
  • add_item() / remove_item() / show_inventory()
  • describe_room() — formatted room description
""",
    2: """Topic 03 — Arrays & Plotting

A numpy array is like a Python list but designed for maths. It lets you work with large grids of numbers quickly.

    import numpy as np
    rooms = np.array([0, 1, 0, 2, 1])

matplotlib lets you draw charts from data:

    plt.plot(hp_history)
    plt.show()

The game uses a 1D numpy array to represent dungeon rooms, and plots enemy HP across a fight so you can see how damage adds up.

New in this topic:
  • DUNGEON_ROOMS — 1D numpy array
  • plot_combat() — draws enemy HP over turns
""",
    3: """Topic 04 — 2D Arrays & Functions

A 2D array is a grid — rows and columns, like a spreadsheet. You access cells with grid[row, col].

A function is a named, reusable block of code:

    def move(direction, pos, grid):
        ...

Once defined, you call it by name. This avoids repeating the same logic everywhere.

The game's dungeon becomes a proper 5x5 grid, and the player can navigate it by typing 'move north', 'attack', etc. This is the first file where the game is actually playable.

New in this topic:
  • DUNGEON_GRID — 5x5 numpy array
  • move(), combat(), display_map()
  • main() — the playable game loop
""",
    4: """Topic 05 — Files & Grids

Files let a program remember data between runs. Python opens files with open():

    with open("save_game.txt", "w") as f:
        f.write(data)

Reading works the same way with "r" instead of "w".

The game can now save your progress to save_game.txt and load it again next time. The dungeon layout is also read from dungeon_map.txt instead of being hard-coded.

New in this topic:
  • save_game() — writes hero state to file
  • load_game() — reads it back
  • load_dungeon_from_file() — reads dungeon_map.txt
  • Commands: save, load
""",
    5: """Topic 06 — Classes & Objects

A class is a blueprint for creating objects. Each object has its own data (attributes) and behaviour (methods):

    class Hero:
        def __init__(self, name):
            self.hp = 100
            self.attack = 10

        def display_stats(self):
            print(f"{self.name}: {self.hp} HP")

Instead of loose variables (NAME, HP, GOLD), the hero is now a single Hero object. The same for enemies and items.

New in this topic:
  • Hero class — name, hp, attack, gold, inventory, position
  • Enemy class — name, hp, attack, gold_drop
  • Item class — name, description, value
  • hero.attack_enemy(enemy) replaces the raw formula
""",
    6: """Topic 07 — Inheritance & Exceptions

Inheritance lets one class extend another. A subclass gets everything from its parent and can add or override behaviour:

    class Goblin(Enemy):
        def __init__(self):
            super().__init__(name="Goblin", hp=20, attack=5, gold_drop=10)

try/except catches errors so the program doesn't crash on bad input:

    try:
        command = input("> ")
    except (EOFError, KeyboardInterrupt):
        return "quit"

New in this topic:
  • Goblin and Dragon subclasses of Enemy
  • Room class — wraps a cell with its occupant
  • safe_input() — wraps input() in try/except
""",
    7: """Topic 08 — Scripts & argparse

argparse lets a Python file read command-line flags when you run it:

    python topic_08.py --name Gandalf --difficulty hard

This turns a script into a configurable program. The dungeon is also auto-generated procedurally instead of read from a file.

New in this topic:
  • parse_args() — --name, --difficulty, --size flags
  • generate_dungeon() — creates a random dungeon grid
  • main(args=None) pattern so the file still works when imported
""",
    8: """Topic 09 — Testing

A test checks that a function does what you expect. Python's unittest module gives you a structured way to write them:

    class TestCombat(unittest.TestCase):
        def test_damage_is_positive(self):
            result = calc_damage(10)
            self.assertGreater(result, 0)

Run all tests with:  python -m unittest topic_09 -v

Tests catch bugs before users do. Every function in the game gets at least one test here.

New in this topic:
  • 18 unit tests across 6 TestCase classes
  • Tests for: damage, movement, inventory, Hero, enemies, dungeon generation
""",
    9: """Topic 10 — pandas Analytics

pandas is a library for working with tabular data — think Excel in Python. You create a DataFrame from a list of dicts:

    import pandas as pd
    df = pd.DataFrame(battle_log)
    print(df.groupby("enemy")["damage"].mean())

The game now logs every battle and uses pandas to show statistics: win rate, average damage dealt, most-killed enemy type.

New in this topic:
  • BATTLE_LOG — list of dicts, one per fight
  • log_battle() — appends to the log
  • analyse_battles() — prints stats, returns DataFrame
  • plot_analytics() — bar chart + pie chart
""",
    10: """Topic 11 — Algorithms & Heatmaps

BFS (Breadth-First Search) is an algorithm that finds the shortest path through a grid. It uses a queue to explore rooms layer by layer:

    from collections import deque
    queue = deque([(start, [start])])

A heatmap colours each cell by how many times it was visited — rooms you explore a lot appear brighter.

New in this topic:
  • bfs_pathfind() — returns shortest path to a target
  • find_nearest_enemy() — locates closest enemy cell
  • generate_dungeon_procedural() — random-walk dungeon
  • plot_heatmap() — matplotlib heatmap of explored rooms
  • Commands: pathfind, heatmap
""",
}


class DungeonLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("COMP1005 Dungeon Launcher")
        self.root.geometry("1200x750")
        self.root.configure(bg=BG_DARK)
        self.dungeon_dir = os.path.dirname(os.path.abspath(__file__))
        self.proc = None
        self._reader_thread = None
        self._build_layout()
        self._configure_highlight_tags()
        self.listbox.selection_set(0)
        self._select_topic(0)

    def _build_layout(self):
        outer = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=BG_DARK,
                               sashwidth=4, sashrelief=tk.FLAT)
        outer.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(outer, bg=BG_DARK)
        tk.Label(left_frame, text="Topics", bg=BG_DARK, fg="#9cdcfe",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=8, pady=(8, 2))
        self.listbox = tk.Listbox(
            left_frame, bg="#252526", fg=FG_DEFAULT,
            selectbackground="#094771", selectforeground="white",
            font=FONT_LIST, borderwidth=0, highlightthickness=0,
            activestyle="none",
        )
        for label in TOPIC_LABELS:
            self.listbox.insert(tk.END, "  " + label)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))
        self.listbox.bind("<ButtonRelease-1>", self._on_listbox_click)
        outer.add(left_frame, minsize=180)

        mid_frame = tk.Frame(outer, bg=BG_DARK)
        tk.Label(mid_frame, text="Explanation", bg=BG_DARK, fg="#9cdcfe",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=8, pady=(8, 2))
        self.explain_text = scrolledtext.ScrolledText(
            mid_frame, bg="#252526", fg=FG_DEFAULT, font=FONT_EXPLAIN,
            wrap=tk.WORD, state=tk.DISABLED, borderwidth=0,
            highlightthickness=0, padx=10, pady=10,
        )
        self.explain_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))
        outer.add(mid_frame, minsize=260)

        right_outer = tk.PanedWindow(outer, orient=tk.VERTICAL, bg=BG_DARK,
                                     sashwidth=4, sashrelief=tk.FLAT)
        outer.add(right_outer, minsize=400)

        src_frame = tk.Frame(right_outer, bg=BG_DARK)
        tk.Label(src_frame, text="Source Code", bg=BG_DARK, fg="#9cdcfe",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=8, pady=(8, 2))
        self.src_text = scrolledtext.ScrolledText(
            src_frame, bg=BG_DARK, fg=FG_DEFAULT, font=FONT_CODE,
            state=tk.DISABLED, borderwidth=0, highlightthickness=0,
            padx=10, pady=10,
        )
        self.src_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 4))
        right_outer.add(src_frame, minsize=200)

        term_frame = tk.Frame(right_outer, bg=BG_DARK)
        self._term_label = tk.Label(term_frame, text="Terminal", bg=BG_DARK,
                                    fg="#9cdcfe", font=("Segoe UI", 11, "bold"))
        self._term_label.pack(anchor="w", padx=8, pady=(8, 2))
        self.term = scrolledtext.ScrolledText(
            term_frame, bg=BG_DARK, fg=FG_DEFAULT, font=FONT_CODE,
            state=tk.DISABLED, borderwidth=0, highlightthickness=0,
            padx=10, pady=10,
        )
        self.term.pack(fill=tk.BOTH, expand=True, padx=4, pady=0)
        self.term.bind("<Button-1>", lambda e: self.term_input.focus_set())
        input_row = tk.Frame(term_frame, bg=BG_DARK)
        input_row.pack(fill=tk.X, padx=4, pady=(2, 4))
        tk.Label(input_row, text=">", bg=BG_DARK, fg="#569cd6",
                 font=FONT_CODE).pack(side=tk.LEFT, padx=(0, 4))
        self.term_input = tk.Entry(
            input_row, bg="#252526", fg=FG_DEFAULT, font=FONT_CODE,
            insertbackground="white", borderwidth=0,
            highlightthickness=1, highlightcolor="#569cd6",
            highlightbackground="#3a3a3a",
        )
        self.term_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.term_input.bind("<Return>", self._on_return)
        right_outer.add(term_frame, minsize=150)

    def _configure_highlight_tags(self):
        if not PYGMENTS_AVAILABLE:
            return
        for token_str, color in TOKEN_COLORS.items():
            self.src_text.tag_configure(token_str, foreground=color)

    def _on_listbox_click(self, event):
        self.listbox.unbind("<ButtonRelease-1>")
        selection = self.listbox.curselection()
        if selection:
            self._select_topic(selection[0])
        self.listbox.after(
            300, lambda: self.listbox.bind("<ButtonRelease-1>", self._on_listbox_click)
        )

    def _select_topic(self, index):
        self._load_explanation(index)
        self._load_source(index)
        self._start_terminal(index)

    def _load_explanation(self, index):
        self.explain_text.config(state=tk.NORMAL)
        self.explain_text.delete("1.0", tk.END)
        self.explain_text.insert(tk.END, EXPLANATIONS.get(index, "No explanation available."))
        self.explain_text.config(state=tk.DISABLED)

    def _load_source(self, index):
        path = os.path.join(self.dungeon_dir, TOPIC_FILES[index])
        self.src_text.config(state=tk.NORMAL)
        self.src_text.delete("1.0", tk.END)
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
        except FileNotFoundError:
            self.src_text.insert(tk.END, f"File not found:\n{path}")
            self.src_text.config(state=tk.DISABLED)
            return
        if PYGMENTS_AVAILABLE:
            lexer = Python3Lexer()
            for token, value in lex(code, lexer):
                self.src_text.insert(tk.END, value, str(token))
        else:
            self.src_text.insert(tk.END,
                "(Install pygments for syntax highlighting: pip install pygments)\n\n")
            self.src_text.insert(tk.END, code)
        self.src_text.config(state=tk.DISABLED)

    def _start_terminal(self, index):
        self._stop_proc()
        fname = TOPIC_FILES[index]
        self._term_label.config(
            text=f"Terminal — {fname}  (type below, Enter to send)"
        )
        self.term.config(state=tk.NORMAL)
        self.term.delete("1.0", tk.END)
        self.term.insert(tk.END, f"Starting {fname} …\n")
        self.term.config(state=tk.DISABLED)
        self.term_input.delete(0, tk.END)
        self.term_input.focus_set()
        try:
            self.proc = subprocess.Popen(
                [sys.executable, "-u", fname],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self.dungeon_dir,
            )
        except Exception as e:
            self.term.config(state=tk.NORMAL)
            self.term.insert(tk.END, f"Could not start {fname}:\n{e}\n")
            self.term.config(state=tk.DISABLED)
            return
        proc_ref = self.proc

        def _reader(proc=proc_ref):
            try:
                while True:
                    chunk = proc.stdout.read1(256)
                    if not chunk:
                        break
                    text = chunk.decode("utf-8", errors="replace")
                    self.term.after(0, self._append_output, text)
            except (OSError, ValueError):
                pass

        self._reader_thread = threading.Thread(target=_reader, daemon=True)
        self._reader_thread.start()

    def _append_output(self, text):
        self.term.config(state=tk.NORMAL)
        self.term.insert(tk.END, text)
        self.term.see(tk.END)
        self.term.config(state=tk.DISABLED)

    def _on_return(self, event):
        line = self.term_input.get()
        self.term_input.delete(0, tk.END)
        self._append_output(line + "\n")
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.stdin.write((line + "\n").encode("utf-8"))
                self.proc.stdin.flush()
            except (BrokenPipeError, OSError):
                pass
        return "break"

    def _stop_proc(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None

    def destroy(self):
        try:
            self._stop_proc()
        finally:
            self.root.destroy()


def main():
    root = tk.Tk()
    app = DungeonLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.destroy)
    root.mainloop()


if __name__ == "__main__":
    main()
