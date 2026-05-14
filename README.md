# Learn-Python Dungeon (COMP1005 Workshop)

This folder contains a topic-by-topic Python “dungeon adventure” built for COMP1005. It teaches core programming concepts step-by-step across 11 topics:

1. Variables & I/O
2. Strings & Lists
3. Arrays & Plotting (NumPy + Matplotlib)
4. 2D Arrays & Functions (first playable grid game loop)
5. Files & Grids (load/save + dungeon_map.txt)
6. Classes & Objects
7. Inheritance & Exceptions
8. Scripts & argparse (procedural dungeon generation)
9. Testing (unittest)
10. pandas Analytics (battle log + summary charts)
11. Algorithms & Heatmaps (BFS pathfinding + exploration heatmap)

Main entry point: the Tkinter GUI launcher (launcher.py). It shows per-topic explanations, the topic source code, and a live Terminal connected to the running topic program.

## Requirements

- Python 3.x
- tkinter (comes with most standard Python installs)
- Python packages: see requirements.txt

Install packages:
pip install -r requirements.txt

## How to run

### GUI launcher
From inside Workshops/dungeon/:
python launcher.py

### Run a topic directly (CLI)
From inside Workshops/dungeon/:
python topic_04.py

## Testing (Topic 09)
From inside Workshops/dungeon/:
python -m unittest topic_09 -v
