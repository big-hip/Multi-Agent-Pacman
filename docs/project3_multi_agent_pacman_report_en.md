# Project 3 Report: Multi-Agent Pacman

## Basic Information

**Course:** Artificial Intelligence Algorithms and Models, Course Project 2026 Spring  
**Selected Project:** Project 3, Multi-Agent Pacman  
**Team Members:** Jin Yuxin and another team member  
**Project Source Code:** UC Berkeley CS188 Multi-Agent Pacman project, extended and completed in this repository  
**Main Implementation File:** `multiAgents.py`

This report describes our course project on Multi-Agent Pacman. The project is based on the classic UC Berkeley CS188 Multi-Agent Search assignment. In this environment, Pacman must make decisions in a maze with food pellets, capsules, walls, and multiple ghosts. The ghosts may behave randomly or directionally, and Pacman must choose actions that balance survival, score maximization, food collection, capsule usage, and ghost avoidance or ghost chasing.

The official course requirement asks each student or group to choose one project, design algorithms to solve the selected problem, submit runnable source code, write a report of no less than 2000 words, prepare slides, and provide a handbook explaining how to build the environment and reproduce the results. For Project 3, the requirement is to complete the project stated at `http://ai.berkeley.edu/multiagent.html`, design at least three algorithms per person, test these algorithms, output the results, and compare their solution quality and time complexity.

Because this is a two-person project, we organized the implementation into six algorithmic components. Jin Yuxin was responsible for the first three components, while I was responsible for the last three components. The six components are:

1. Reflex Agent
2. Minimax Agent
3. Alpha-Beta Agent
4. Expectimax Agent
5. Better Evaluation Function
6. Contest Agent, a risk-aware expectimax extension

My individual contribution focuses on the last three components: Expectimax Agent, Better Evaluation Function, and Contest Agent. These components are especially important because they move the project from pure adversarial search toward more realistic probabilistic decision making and heuristic evaluation design. Expectimax models ghosts as stochastic agents, the better evaluation function provides a stronger state-scoring model, and Contest Agent extends expectimax with a more realistic probability model for directional ghosts.

## 1. Problem Description

Multi-Agent Pacman is a sequential decision-making problem in a dynamic multi-agent environment. The world is represented as a grid maze. Pacman is controlled by our algorithm and has legal actions such as moving north, south, east, west, or stopping. Ghosts are other agents in the same environment. Pacman receives positive score by eating food pellets, eating capsules, and completing the maze. Pacman receives negative effects from time steps and from being caught by active ghosts. If Pacman eats a capsule, ghosts become scared for a limited number of moves, and Pacman can chase and eat them for extra reward.

The central difficulty is that Pacman is not acting alone. Each move by Pacman is followed by moves from one or more ghosts. Therefore, Pacman's best action depends not only on the immediate successor state, but also on what the ghosts may do later. This makes the problem a multi-agent search problem instead of a simple single-agent path planning problem.

The environment creates several important AI modeling questions:

1. How should Pacman evaluate a state?
2. Should ghosts be modeled as adversarial agents or random agents?
3. How deep should Pacman search before using an evaluation function?
4. How can the search avoid unnecessary computation?
5. How can heuristic features be combined to improve real game performance?

Different algorithms answer these questions differently. Minimax assumes that ghosts always choose the worst possible action for Pacman. Alpha-beta pruning keeps the same adversarial assumption but reduces the number of expanded branches. Expectimax assumes that ghosts choose actions probabilistically and optimizes expected utility. A reflex agent does not perform deep search and only evaluates immediate successor states. A better evaluation function improves the quality of terminal or depth-limited state estimates. Our Contest Agent adds another layer of realism by assigning higher probability to ghost actions that are consistent with `DirectionalGhost` behavior.

Although the project description in the course PDF contains a line saying "test these algorithms on the 8 puzzle problem", this appears to be inherited from Project 2. For Project 3, the correct test environment is Multi-Agent Pacman, so all experiments in this report are performed on Pacman layouts and Pacman agents.

## 2. Project Structure

The main source file for our implementation is:

```text
multiAgents.py
```

The project also includes the following important files:

```text
pacman.py
game.py
ghostAgents.py
util.py
layouts/
test_cases/
autograder.py
```

`pacman.py` provides the game runner and command-line interface. `game.py` defines common game abstractions such as agents, directions, actions, and game states. `ghostAgents.py` defines ghost behaviors such as `RandomGhost` and `DirectionalGhost`. `util.py` provides helper data structures and utility functions, including Manhattan distance. `layouts/` stores map files, and `test_cases/` stores autograder tests. The official grading framework is provided by `autograder.py`.

The core design is centered around `GameState`. Each search algorithm receives a current `GameState`, enumerates legal actions, generates successor states, evaluates future outcomes, and returns the selected Pacman action. Pacman is always agent index 0. Ghosts are indexed from 1 to `gameState.getNumAgents() - 1`.

## 3. Team Division of Work

The six algorithmic components were divided as follows:

| Component | Main Idea | Responsible Member |
|---|---|---|
| Reflex Agent | Evaluate one-step successor states | Jin Yuxin |
| Minimax Agent | Adversarial search with max and min layers | Jin Yuxin |
| Alpha-Beta Agent | Minimax with pruning | Jin Yuxin |
| Expectimax Agent | Probabilistic search for random ghosts | My implementation |
| Better Evaluation Function | Heuristic state evaluation | My implementation |
| Contest Agent | Risk-aware expectimax for directional ghosts | My implementation |

This division satisfies the requirement that each member contributes at least three algorithmic components. In addition, the implementation keeps the algorithms comparable by using the same Pacman environment, the same action interface, and a consistent depth definition.

## 4. Algorithm 1: Reflex Agent

The Reflex Agent chooses an action by evaluating only the immediate successor state. It does not build a full search tree. For each legal Pacman action, the agent generates the successor state and calculates a heuristic score. The action with the highest score is selected. If multiple actions have the same best score, the agent randomly chooses one among them.

The evaluation function uses several features:

1. The game score of the successor state.
2. The distance from Pacman to the nearest food pellet.
3. The distance from Pacman to each ghost.
4. Whether a ghost is scared.
5. A penalty for the `STOP` action.

The Reflex Agent is simple and fast. Its time complexity is approximately linear in the number of legal Pacman actions and the number of food and ghost positions used in the evaluation. Because it has no deep lookahead, it may fail in situations where a locally attractive action leads to danger in a few future moves. However, with a reasonable evaluation function, it performs well on simple layouts.

## 5. Algorithm 2: Minimax Agent

The Minimax Agent models the game as an adversarial search problem. Pacman is the maximizing agent, and ghosts are minimizing agents. The algorithm recursively explores the game tree up to a fixed depth. At Pacman's turn, it chooses the maximum value among successor states. At each ghost's turn, it chooses the minimum value, representing the assumption that the ghost will act in the worst possible way for Pacman.

The important implementation detail is the depth definition. In a multi-agent setting, one depth level should correspond to one complete round of actions by all agents, not a single individual move. Therefore, the depth is increased only when the turn cycles back to Pacman after all ghosts have moved. This keeps the search depth consistent across layouts with different numbers of ghosts.

The terminal conditions are:

1. Pacman wins.
2. Pacman loses.
3. The search reaches the depth limit.
4. An agent has no legal action.

The advantage of Minimax is that it provides a robust strategy against adversarial ghosts. The disadvantage is that it can be too conservative when ghosts are actually random. It also has high computational cost. If the average branching factor is `b`, the number of agents is `n`, and the depth is `d` Pacman rounds, the time complexity is roughly `O(b^(n*d))`.

## 6. Algorithm 3: Alpha-Beta Agent

Alpha-Beta Agent improves Minimax by pruning branches that cannot affect the final decision. It still returns the same optimal action as Minimax under the same evaluation function and move ordering, but it avoids evaluating some unnecessary branches.

The algorithm maintains two bounds:

1. `alpha`: the best value currently guaranteed for the maximizing player.
2. `beta`: the best value currently guaranteed for the minimizing player.

At a Pacman max layer, if the current value becomes larger than beta, further exploration is unnecessary because a previous min layer would avoid this branch. At a ghost min layer, if the current value becomes smaller than alpha, further exploration is unnecessary because a previous max layer would avoid this branch.

Alpha-beta pruning is especially useful in game search because it reduces computation while preserving decision correctness under the minimax model. In the best case, good move ordering can reduce the effective search complexity substantially. In the worst case, the complexity remains similar to Minimax, but in practice it is usually faster.

## 7. Algorithm 4: Expectimax Agent

Expectimax Agent is one of my main implemented components. It changes the ghost model from adversarial to probabilistic. Instead of assuming that every ghost always chooses the worst action for Pacman, Expectimax assumes that each ghost chooses uniformly at random from its legal actions.

The search tree has two types of layers:

1. Max layers for Pacman.
2. Chance layers for ghosts.

At a Pacman layer, the algorithm returns the maximum successor value. At a ghost layer, the algorithm returns the expected value over all legal ghost actions. If a ghost has `k` legal actions and is modeled uniformly, each action has probability `1/k`.

The recursive value function can be summarized as:

```text
V(s) = evaluation(s), if s is terminal or depth limit is reached
V(s) = max_a V(successor(s, a)), if the current agent is Pacman
V(s) = average_a V(successor(s, a)), if the current agent is a ghost
```

Expectimax is more realistic when ghosts are random or partially random. In many Pacman layouts, ghosts are not perfect adversarial optimizers. Therefore, a purely minimax strategy may be too defensive. Expectimax can take actions that have high expected reward even if there exists a low-probability bad outcome.

The implementation supports any number of ghosts through agent index rotation. After each agent acts, the next agent index is computed by `(agentIndex + 1) % numAgents`. The depth is increased only when the next agent becomes Pacman again. This matches the same depth semantics used by Minimax and Alpha-Beta.

The time complexity of Expectimax is similar to Minimax because it still explores the same tree structure. If the branching factor is `b`, number of agents is `n`, and Pacman depth is `d`, the complexity is approximately `O(b^(n*d))`. The main difference is not the asymptotic cost, but the value backup rule at ghost nodes.

## 8. Algorithm 5: Better Evaluation Function

The Better Evaluation Function is another major part of my implementation. In depth-limited search, the algorithm cannot search all the way to a final win or loss. Therefore, the quality of the evaluation function strongly affects the quality of the decision. A weak evaluation function may make a good search algorithm behave poorly.

The evaluation function combines the following features:

1. Current game score.
2. Number of remaining food pellets.
3. Distance to the closest food pellet.
4. Number of remaining capsules.
5. Distance to the closest capsule.
6. Distance to active ghosts.
7. Distance to scared ghosts.
8. Win and loss terminal states.

The design goal is to balance three objectives:

1. Safety: avoid active ghosts, especially when they are very close.
2. Efficiency: reduce the number of remaining food pellets and capsules.
3. Reward seeking: chase scared ghosts when the opportunity is safe and useful.

The function returns positive infinity for winning states and negative infinity for losing states. This ensures that terminal wins and losses dominate ordinary heuristic features. For food, the function rewards being close to the nearest food and penalizes having many remaining food pellets. This encourages Pacman not only to move toward food, but also to finish the board. For capsules, the function rewards proximity and penalizes remaining capsule count. Capsules are important because they can transform a dangerous situation into an opportunity to chase ghosts.

Ghost handling is the most important part. If a ghost is active, the function penalizes proximity. If the ghost is at distance zero, the state is losing and receives negative infinity. If a ghost is scared, proximity becomes beneficial because Pacman may eat the ghost for extra score. This feature switching is essential because the same spatial relation has opposite meaning depending on the ghost's scared timer.

This evaluation function improves solution quality because it provides a richer estimate than the raw game score. It also remains computationally efficient. It mainly scans food, capsules, and ghosts, so its cost is roughly linear in the number of relevant objects on the board.

## 9. Algorithm 6: Contest Agent

The Contest Agent is the extra algorithmic component added to make the project stronger and to create a clear sixth component for the two-person division. It is my third major contribution together with Expectimax and Better Evaluation Function.

Contest Agent is a risk-aware expectimax agent. The standard Expectimax Agent assumes that ghosts choose uniformly at random. However, the optional contest environment uses `DirectionalGhost`, which is not purely random. A `DirectionalGhost` tends to move toward Pacman when active and tends to move away from Pacman when scared. Therefore, a uniform ghost model is not accurate enough.

Contest Agent keeps the expectimax structure but changes the probability distribution at ghost nodes. For each legal ghost action, the algorithm generates the successor state and measures the Manhattan distance between the ghost and Pacman. If the ghost is active, actions that reduce the distance to Pacman are treated as preferred actions. If the ghost is scared, actions that increase the distance from Pacman are treated as preferred actions.

The model assigns most probability mass to preferred actions and a smaller probability mass to all legal actions. In our implementation, the directional behavior probability is set to 0.8, and the remaining 0.2 probability is distributed uniformly. This makes the ghost model more realistic than uniform expectimax while still allowing uncertainty.

The backup rule at Pacman's layer remains maximization. At ghost layers, the value is the weighted expectation:

```text
V(s) = sum over actions a of P(a | s, ghost) * V(successor(s, a))
```

Contest Agent also avoids choosing `STOP` for Pacman when other legal actions exist. This prevents Pacman from wasting time unless stopping is the only legal action. The evaluation function used by Contest Agent, `contestEvaluationFunction`, is more aggressive than the basic better evaluation function. It uses stronger penalties for nearby active ghosts and stronger incentives to finish the board efficiently.

Compared with standard Expectimax, Contest Agent has the same asymptotic search complexity, but it spends slightly more time at ghost nodes because it must compute action weights. The additional cost is small because the number of legal ghost actions is limited. In return, the algorithm has a more accurate opponent model for `DirectionalGhost`.

## 10. Experimental Setup

We used the official autograder and direct Pacman command-line experiments.

The core autograder commands are:

```powershell
python autograder.py -q q1 --no-graphics
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
```

The direct command for running the Contest Agent is:

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

We also used direct gameplay commands for quick checks, such as:

```powershell
python pacman.py -p ReflexAgent -l testClassic -n 10 -q
python pacman.py -p ExpectimaxAgent -l smallClassic -a depth=2 -q
```

All experiments were performed in the same project folder. The source code is runnable without modifying the original game engine. The main dependency is Python. The implementation uses only standard project files and does not require a large external dataset. The Pacman layouts under `layouts/` serve as the test environments.

## 11. Performance Results

The official autograder results for the five standard CS188 tasks are:

| Question | Component | Score |
|---|---|---|
| Q1 | Reflex Agent | 4/4 |
| Q2 | Minimax Agent | 5/5 |
| Q3 | Alpha-Beta Agent | 5/5 |
| Q4 | Expectimax Agent | 5/5 |
| Q5 | Better Evaluation Function | 6/6 |
| Total | Standard Project Score | 25/25 |

For Q1, the Reflex Agent achieved an average score of 1276.0 and won 10 out of 10 games in the autograder test. For Q5, the Better Evaluation Function achieved an average score of 1178.3 and won 10 out of 10 games. These results show that the evaluation functions are not only syntactically correct but also effective in gameplay.

For Q2 to Q4, the autograder focuses mainly on search correctness, value propagation, depth handling, multi-ghost rotation, and generated successor behavior. In the official tests, these agents passed all correctness checks. Some single demonstration games on `smallClassic` may still result in a loss, but this does not mean the algorithm is incorrect. The reason is that the autograder evaluates whether the search procedure follows the expected semantics, while a single game result depends on the map, ghost behavior, depth limit, and evaluation function.

The Contest Agent was evaluated with:

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

The observed result was:

| Agent | Layout | Ghost Type | Games | Average Score | Win Rate |
|---|---|---|---:|---:|---:|
| ContestAgent | contestClassic | DirectionalGhost | 5 | 1261.4 | 2/5 |

This result shows that Contest Agent is runnable and can win games in the more difficult contest setting. It is not tuned as a final competition-winning agent, but it demonstrates a meaningful algorithmic extension beyond the five standard tasks. The result also shows an important practical lesson: a more realistic ghost model improves reasoning, but performance still depends heavily on evaluation weights, search depth, and map structure.

## 12. Comparison of Algorithms

The algorithms differ in both solution quality and computational complexity.

Reflex Agent is the fastest. It only evaluates immediate successor states, so it can make decisions quickly. However, it cannot anticipate traps several moves ahead. Its quality depends strongly on the local evaluation function.

Minimax Agent is more strategic because it searches future states and assumes adversarial ghosts. It is robust against worst-case ghost behavior. However, this assumption can be too pessimistic, and the search cost grows exponentially with depth and number of agents.

Alpha-Beta Agent keeps the same decision model as Minimax but improves efficiency through pruning. It is especially useful when the search tree is large. Its final action is consistent with Minimax, but it can avoid exploring branches that cannot affect the root decision.

Expectimax Agent is more suitable for random ghosts. It optimizes expected value instead of worst-case value. This allows it to choose actions that are too risky under Minimax but reasonable under probabilistic behavior. Its cost is still exponential because it must explore chance branches.

Better Evaluation Function is not a complete search algorithm by itself, but it is essential for depth-limited search quality. It provides a stronger estimate of non-terminal states by combining score, food, capsules, and ghost features. A good evaluation function can make shallow search behave much better.

Contest Agent extends Expectimax by using a non-uniform probability model for ghosts. It is better aligned with `DirectionalGhost` behavior than uniform Expectimax. Its complexity is similar to Expectimax, with a small additional cost for computing ghost action weights. It represents a more realistic model-based decision-making approach.

## 13. Environment and Running Handbook

### 13.1 Environment

Recommended environment:

```text
Python 3.x
Windows PowerShell or another terminal
Project folder containing pacman.py, multiAgents.py, layouts/, and test_cases/
```

No external dataset is required. The maps in `layouts/` are the test environments.

### 13.2 Build and Setup

Enter the project directory:

```powershell
cd "D:\桌面\研一\研一的课\人工智能算法与模型\multiagent"
```

If a dependency file is provided, install dependencies with:

```powershell
pip install -r requirements.txt
```

For this project, the implementation mainly uses the provided Pacman framework and standard Python modules.

### 13.3 Run Standard Tests

Run all standard autograder tests:

```powershell
python autograder.py
```

Run individual tests:

```powershell
python autograder.py -q q1 --no-graphics
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
```

### 13.4 Run Individual Agents

Run Reflex Agent:

```powershell
python pacman.py -p ReflexAgent -l testClassic -n 10 -q
```

Run Minimax Agent:

```powershell
python pacman.py -p MinimaxAgent -l smallClassic -a depth=2 -q
```

Run Alpha-Beta Agent:

```powershell
python pacman.py -p AlphaBetaAgent -l smallClassic -a depth=2 -q
```

Run Expectimax Agent:

```powershell
python pacman.py -p ExpectimaxAgent -l smallClassic -a depth=2 -q
```

Run Expectimax with the better evaluation function:

```powershell
python pacman.py -p ExpectimaxAgent -l smallClassic -a evalFn=betterEvaluationFunction,depth=2 -q
```

Run Contest Agent:

```powershell
python pacman.py -p ContestAgent -l contestClassic -g DirectionalGhost -k 3 -n 5 -q
```

## 14. Conclusion

This project implements and evaluates a set of multi-agent decision-making algorithms in the Pacman environment. The completed system includes reflex decision making, adversarial minimax search, alpha-beta pruning, probabilistic expectimax search, heuristic evaluation design, and a risk-aware expectimax extension. The standard autograder score is 25/25, showing that the required algorithms satisfy the correctness tests.

My main contribution is the implementation and analysis of the last three components: Expectimax Agent, Better Evaluation Function, and Contest Agent. Expectimax changes the ghost model from worst-case adversarial behavior to stochastic behavior. The better evaluation function improves the quality of depth-limited decisions by combining food, capsule, score, and ghost features. Contest Agent further improves the opponent model by assigning non-uniform probabilities to directional ghost actions.

The experiments show that different assumptions lead to different behavior. Minimax is safe but conservative. Alpha-beta is more efficient while preserving minimax correctness. Expectimax is more suitable for random ghosts. Heuristic evaluation is crucial for real gameplay performance. Contest Agent demonstrates how domain knowledge about ghost behavior can be incorporated into the search process.

Overall, this project helped us understand the practical relationship between search algorithms, opponent modeling, heuristic evaluation, and empirical performance. It also shows that in multi-agent AI systems, a good algorithm is not only a formal search procedure, but also a carefully designed combination of state representation, action modeling, evaluation features, and computational trade-offs.
