# 8-Puzzle Search Experiment Report

## Background
This experiment evaluates multiple search strategies on the 8-puzzle problem. The objective is to compare solution quality and empirical time complexity using the same test instances.

## Tasks
- Implement at least 3 search algorithms.
- Test algorithms on 8-puzzle instances and output solutions.
- Compare solution quality and time complexity.

## Implemented Algorithms
- BFS
- IDS (Iterative Deepening DFS)
- A* (Manhattan Heuristic)
- Greedy Best-First (Manhattan Heuristic)

## Test Results

### Case-1-Easy

| Algorithm | Solved | Path Length | Expanded | Generated | Time (s) | Path |
|---|---:|---:|---:|---:|---:|---|
| BFS | True | 1 | 4 | 8 | 0.000032 | R |
| IDS | True | 1 | 5 | 4 | 0.000011 | R |
| A*_Manhattan | True | 1 | 2 | 4 | 0.000080 | R |
| Greedy_Best_First | True | 1 | 2 | 4 | 0.000068 | R |

### Case-2-Medium

| Algorithm | Solved | Path Length | Expanded | Generated | Time (s) | Path |
|---|---:|---:|---:|---:|---:|---|
| BFS | True | 5 | 47 | 76 | 0.000092 | DLURD |
| IDS | True | 5 | 95 | 90 | 0.000126 | DLURD |
| A*_Manhattan | True | 5 | 6 | 12 | 0.000036 | DLURD |
| Greedy_Best_First | True | 5 | 6 | 12 | 0.000030 | DLURD |

### Case-3-Harder

| Algorithm | Solved | Path Length | Expanded | Generated | Time (s) | Path |
|---|---:|---:|---:|---:|---:|---|
| BFS | True | 7 | 116 | 207 | 0.000227 | ULLDDRR |
| IDS | True | 7 | 269 | 262 | 0.000274 | ULLDDRR |
| A*_Manhattan | True | 7 | 8 | 13 | 0.000043 | ULLDDRR |
| Greedy_Best_First | True | 7 | 8 | 13 | 0.000034 | ULLDDRR |

## Analysis
- Solution quality: BFS/IDS/A* consistently return shortest paths on these unit-cost instances. Greedy may return longer paths in general, even if some cases happen to match optimal depth.
- Time complexity (empirical): A* expands far fewer nodes than BFS/IDS on harder cases due to informed heuristic guidance.
- IDS can find optimal depth with low memory but often repeats expansions across depth limits.
- Greedy is usually fast but not guaranteed optimal.

## Complexity Discussion
- BFS: Complete and optimal for unit step cost; worst-case time/space are exponential in depth.
- IDS: Complete and optimal for unit step cost; time is exponential with repeated re-expansion, memory is linear in depth.
- A*: Complete and optimal with admissible/consistent heuristic (Manhattan); practical performance is usually best among optimal methods.
- Greedy Best-First: Not optimal; often explores fewer nodes but can be misled by local heuristic choices.