# Project Handbook: Multi-Agent Pacman

## 1. Project Information

**Course:** Artificial Intelligence Algorithms and Models, Course Project 2026 Spring  
**Selected Project:** Project 3, Multi-Agent Pacman  
**Team Members:** Jin Yuxin and another team member  
**Main Source File:** `multiAgents.py`  
**Project Type:** Multi-agent search and evaluation function design

This handbook explains how to build the running environment, how to execute each implemented algorithm, and how to reproduce the experimental results.

## 2. Project Folder Structure

The runnable project folder should contain the following key files and directories:

```text
multiagent/
+-- autograder.py
+-- game.py
+-- ghostAgents.py
+-- graphicsDisplay.py
+-- keyboardAgents.py
+-- layout.py
+-- multiAgents.py
+-- pacman.py
+-- pacmanAgents.py
+-- textDisplay.py
+-- util.py
+-- requirements.txt
+-- layouts/
+-- test_cases/
`-- docs/
```

The most important implementation file is:

```text
multiAgents.py
```

It contains the implemented Pacman agents and evaluation functions.

## 3. Environment Requirements

Recommended environment:

```text
Operating System: Windows, Linux, or macOS
Python: Python 3.x
Terminal: PowerShell, Command Prompt, Bash, or another shell
```

No external dataset is required. The Pacman maps in the `layouts/` folder are used as the experimental environments.

## 4. Environment Setup

First, open a terminal and enter the project directory.

Example on Windows PowerShell:

```powershell
cd "D:\桌面\研一\研一的课\人工智能算法与模型\multiagent"
```

If a Python virtual environment is preferred, create and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies if needed:

```powershell
pip install -r requirements.txt
```

The project mainly uses the provided Pacman framework and standard Python libraries, so it can usually run directly after Python is installed.

## 5. Implemented Algorithms

This project contains six algorithmic components:

| No. | Algorithm or Component | Class or Function |
|---:|---|---|
| 1 | Reflex Agent | `ReflexAgent` |
| 2 | Minimax Search | `MinimaxAgent` |
| 3 | Alpha-Beta Pruning | `AlphaBetaAgent` |
| 4 | Expectimax Search | `ExpectimaxAgent` |
| 5 | Better Evaluation Function | `betterEvaluationFunction` |
| 6 | Risk-Aware Contest Agent | `ContestAgent` |

The first three components are assigned to Jin Yuxin. The last three components are my main contribution.

## 6. Check Whether the Code Can Be Imported

Before running experiments, check that the main implementation file has no syntax error:

```powershell
python -m py_compile multiAgents.py
```

If the command finishes without error output, the file can be imported successfully.

## 7. Run the Official Autograder

To run all standard tests:

```powershell
python autograder.py
```

To run each question separately:

```powershell
python autograder.py -q q1 --no-graphics
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
```

Expected standard autograder results:

| Question | Component | Expected Score |
|---|---|---:|
| q1 | Reflex Agent | 4/4 |
| q2 | Minimax Agent | 5/5 |
| q3 | Alpha-Beta Agent | 5/5 |
| q4 | Expectimax Agent | 5/5 |
| q5 | Better Evaluation Function | 6/6 |
| Total | Standard Project | 25/25 |

## 8. Run Each Algorithm Manually

### 8.1 Reflex Agent

```powershell
python pacman.py -p ReflexAgent -l testClassic -n 10 -q
```

This command runs `ReflexAgent` on `testClassic` for 10 games without graphics.

### 8.2 Minimax Agent

```powershell
python pacman.py -p MinimaxAgent -l smallClassic -a depth=2 -q
```

This command runs adversarial minimax search with search depth 2.

### 8.3 Alpha-Beta Agent

```powershell
python pacman.py -p AlphaBetaAgent -l smallClassic -a depth=2 -q
```

This command runs minimax search with alpha-beta pruning.

### 8.4 Expectimax Agent

```powershell
python pacman.py -p ExpectimaxAgent -l smallClassic -a depth=2 -q
```

This command runs expectimax search. Ghost nodes are modeled as chance nodes with uniformly random actions.

### 8.5 Expectimax Agent with Better Evaluation Function

```powershell
python pacman.py -p ExpectimaxAgent -l smallClassic -a evalFn=betterEvaluationFunction,depth=2 -q
```

This command combines expectimax search with the stronger heuristic evaluation function.

### 8.6 Contest Agent

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

This command runs the additional `ContestAgent` on the `contestClassic` layout with three `DirectionalGhost` agents for five games.

## 9. Reproduce the Reported Results

### 9.1 Reflex Agent Result

Run:

```powershell
python autograder.py -q q1 --no-graphics
```

Expected result:

```text
Question q1: 4/4
Average Score: 1276.0
Win Rate: 10/10
```

### 9.2 Minimax Result

Run:

```powershell
python autograder.py -q q2
```

Expected result:

```text
Question q2: 5/5
```

### 9.3 Alpha-Beta Result

Run:

```powershell
python autograder.py -q q3
```

Expected result:

```text
Question q3: 5/5
```

### 9.4 Expectimax Result

Run:

```powershell
python autograder.py -q q4
```

Expected result:

```text
Question q4: 5/5
```

### 9.5 Better Evaluation Function Result

Run:

```powershell
python autograder.py -q q5
```

Expected result:

```text
Question q5: 6/6
Average Score: 1178.3
Win Rate: 10/10
```

### 9.6 Contest Agent Result

Run:

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

Observed result in our experiment:

```text
Average Score: 1261.4
Win Rate: 2/5
```

The `test_cases/extra` folder in this local copy does not include `grade-agent.solution`, so the optional extra autograder cannot be reproduced directly with `python autograder.py -q extra`. Therefore, the Contest Agent is evaluated with the direct `pacman.py` command above.

## 10. Notes on Graphics Mode

Most commands above use `-q`, which means quiet mode without graphics. This is recommended for fast testing and stable result reproduction.

To view the graphical game window, remove `-q`:

```powershell
python pacman.py -p ReflexAgent -l testClassic -n 1
```

Graphics mode is useful for demonstration, but quiet mode is better for collecting experimental results.

## 11. Common Problems and Solutions

### Problem 1: Python command is not found

Install Python 3.x and make sure it is added to the system PATH. Then reopen the terminal and run:

```powershell
python --version
```

### Problem 2: The terminal is not in the project folder

Use `cd` to enter the folder that contains `pacman.py` and `multiAgents.py`.

### Problem 3: Autograder is slow

Run questions separately:

```powershell
python autograder.py -q q1 --no-graphics
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
```

### Problem 4: Extra autograder reports a missing solution file

The local `test_cases/extra` folder may not include `grade-agent.solution`. Use the direct Contest Agent command instead:

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

## 12. Submission Checklist

The final submission package should include:

1. The whole runnable project folder.
2. Source code, especially `multiAgents.py`.
3. The English project report.
4. The project slides.
5. This project handbook.
6. The provided layouts and test cases.

The folder name should follow the course requirement:

```text
Student Name + Student ID
```

For a two-person group, include both members' names and student IDs if required by the teaching assistant.
