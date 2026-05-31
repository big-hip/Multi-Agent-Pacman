# Dataset Description: Multi-Agent Pacman Layouts and Test Cases

## 1. Overview

This project does not use a conventional tabular dataset. The experiments are based on the official UC Berkeley Multi-Agent Pacman environment. In this environment, the "dataset" consists of maze layouts, game configurations, ghost settings, and autograder test cases.

The data used in this project is stored in:

```text
layouts/
test_cases/
```

The `layouts/` directory defines Pacman maps. Each map specifies walls, food pellets, capsules, Pacman starting position, and ghost starting positions. The `test_cases/` directory defines structured tests for different agents and algorithms.

## 2. Layout Data

The layout files are plain-text maze files with the `.lay` extension.

Important layouts include:

| Layout File | Purpose |
|---|---|
| `testClassic.lay` | Used for testing Reflex Agent gameplay performance |
| `smallClassic.lay` | Used for search agent demonstrations |
| `minimaxClassic.lay` | Used for minimax-related experiments |
| `openClassic.lay` | Used by the q1 Reflex Agent autograder |
| `contestClassic.lay` | Used for the additional Contest Agent experiment |

Common symbols in layout files:

| Symbol | Meaning |
|---|---|
| `%` | Wall |
| `.` | Food pellet |
| `o` | Capsule |
| `P` | Pacman starting position |
| `G` | Ghost starting position |
| Space | Empty path |

Example:

```text
%%%%%%%%%%%%%%%%%%%%
%o...%........%...o%
%.%%.%.%%..%%.%.%%.%
%...... G GG%......%
%.%.%%.%% %%%.%%.%.%
%.%....% ooo%.%..%.%
%.%.%%.% %% %.%.%%.%
%o%......P....%....%
%%%%%%%%%%%%%%%%%%%%
```

This example is from `layouts/contestClassic.lay`.

## 3. Test Case Data

The `test_cases/` directory contains autograder test definitions and expected solution files. These files are used to evaluate whether the implemented agents follow the required search semantics.

Main test groups:

| Test Group | Evaluated Component |
|---|---|
| `q1` | Reflex Agent |
| `q2` | Minimax Agent |
| `q3` | Alpha-Beta Agent |
| `q4` | Expectimax Agent |
| `q5` | Better Evaluation Function |
| `extra` | Optional Contest Agent configuration |

The standard tests check:

1. Correct action selection.
2. Correct value backup.
3. Correct depth handling.
4. Correct multi-ghost agent rotation.
5. Correct behavior on win and loss states.
6. Gameplay performance for evaluation functions.

## 4. How the Dataset Is Used

The algorithms interact with the dataset through the Pacman game engine:

1. A layout file is loaded from `layouts/`.
2. The game engine initializes Pacman, ghosts, walls, food, and capsules.
3. The selected Pacman agent receives a `GameState`.
4. The agent searches or evaluates possible successor states.
5. The game records score, win rate, and final outcome.

For autograder tests, the test definitions in `test_cases/` are loaded automatically by:

```powershell
python autograder.py
```

For manual experiments, the layout can be selected with the `-l` argument:

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

## 5. Reproducibility

The dataset is included in the project repository. No extra download is required.

To reproduce the standard results, run:

```powershell
python autograder.py -q q1 --no-graphics
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
```

To reproduce the additional Contest Agent experiment, run:

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

## 6. Dataset License and Attribution

The layouts and test cases are part of the UC Berkeley CS188 Pacman AI Projects. They are used for educational purposes with attribution to UC Berkeley AI:

```text
http://ai.berkeley.edu
```

The original project files state that the project may be used or extended for educational purposes if the license notice and attribution are retained.
