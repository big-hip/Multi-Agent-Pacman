from __future__ import annotations

import random
from dataclasses import dataclass
from time import perf_counter

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVE_DELTA = {"U": -3, "D": 3, "L": -1, "R": 1}


@dataclass
class TrialResult:
    algorithm: str
    case_name: str
    solved: bool
    steps: int
    elapsed_seconds: float
    expanded_nodes: int
    action_trace: str


def is_goal(state: tuple[int, ...]) -> bool:
    return state == GOAL


def manhattan(state: tuple[int, ...]) -> int:
    total = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        gi = tile - 1
        total += abs(i // 3 - gi // 3) + abs(i % 3 - gi % 3)
    return total


def misplaced(state: tuple[int, ...]) -> int:
    return sum(1 for i, v in enumerate(state) if v != 0 and v != GOAL[i])


def evaluate(state: tuple[int, ...]) -> float:
    if is_goal(state):
        return 10_000.0
    # Higher is better for solver agent.
    return -3.0 * manhattan(state) - 1.5 * misplaced(state)


def valid_move(blank: int, action: str) -> bool:
    if action == "U":
        return blank >= 3
    if action == "D":
        return blank <= 5
    if action == "L":
        return blank % 3 != 0
    if action == "R":
        return blank % 3 != 2
    return False


def legal_actions(state: tuple[int, ...]) -> list[str]:
    blank = state.index(0)
    return [a for a in ("U", "D", "L", "R") if valid_move(blank, a)]


def apply_action(state: tuple[int, ...], action: str) -> tuple[int, ...]:
    blank = state.index(0)
    other = blank + MOVE_DELTA[action]
    s = list(state)
    s[blank], s[other] = s[other], s[blank]
    return tuple(s)


class NodeCounter:
    def __init__(self) -> None:
        self.count = 0


def minimax_decision(state: tuple[int, ...], depth: int, counter: NodeCounter) -> str:
    actions = legal_actions(state)
    best_action = actions[0]
    best_val = float("-inf")

    for action in actions:
        succ = apply_action(state, action)
        value = minimax_value(succ, depth, False, counter)
        if value > best_val:
            best_val = value
            best_action = action

    return best_action


def minimax_value(state: tuple[int, ...], depth: int, solver_turn: bool, counter: NodeCounter) -> float:
    counter.count += 1
    if depth == 0 or is_goal(state):
        return evaluate(state)

    actions = legal_actions(state)
    if solver_turn:
        val = float("-inf")
        for action in actions:
            val = max(val, minimax_value(apply_action(state, action), depth - 1, False, counter))
        return val

    val = float("inf")
    for action in actions:
        val = min(val, minimax_value(apply_action(state, action), depth - 1, True, counter))
    return val


def alphabeta_decision(state: tuple[int, ...], depth: int, counter: NodeCounter) -> str:
    actions = legal_actions(state)
    alpha = float("-inf")
    beta = float("inf")
    best_action = actions[0]
    best_val = float("-inf")

    for action in actions:
        succ = apply_action(state, action)
        value = alphabeta_value(succ, depth, False, alpha, beta, counter)
        if value > best_val:
            best_val = value
            best_action = action
        alpha = max(alpha, best_val)

    return best_action


def alphabeta_value(
    state: tuple[int, ...],
    depth: int,
    solver_turn: bool,
    alpha: float,
    beta: float,
    counter: NodeCounter,
) -> float:
    counter.count += 1
    if depth == 0 or is_goal(state):
        return evaluate(state)

    actions = legal_actions(state)
    if solver_turn:
        val = float("-inf")
        for action in actions:
            val = max(val, alphabeta_value(apply_action(state, action), depth - 1, False, alpha, beta, counter))
            if val > beta:
                return val
            alpha = max(alpha, val)
        return val

    val = float("inf")
    for action in actions:
        val = min(val, alphabeta_value(apply_action(state, action), depth - 1, True, alpha, beta, counter))
        if val < alpha:
            return val
        beta = min(beta, val)
    return val


def expectimax_decision(state: tuple[int, ...], depth: int, counter: NodeCounter) -> str:
    actions = legal_actions(state)
    best_action = actions[0]
    best_val = float("-inf")

    for action in actions:
        succ = apply_action(state, action)
        value = expectimax_value(succ, depth, False, counter)
        if value > best_val:
            best_val = value
            best_action = action

    return best_action


def expectimax_value(state: tuple[int, ...], depth: int, solver_turn: bool, counter: NodeCounter) -> float:
    counter.count += 1
    if depth == 0 or is_goal(state):
        return evaluate(state)

    actions = legal_actions(state)
    if solver_turn:
        val = float("-inf")
        for action in actions:
            val = max(val, expectimax_value(apply_action(state, action), depth - 1, False, counter))
        return val

    p = 1.0 / len(actions)
    exp_val = 0.0
    for action in actions:
        exp_val += p * expectimax_value(apply_action(state, action), depth - 1, True, counter)
    return exp_val


def worst_disturbance_action(state: tuple[int, ...]) -> str:
    actions = legal_actions(state)
    worst_action = actions[0]
    worst_value = float("inf")
    for action in actions:
        v = evaluate(apply_action(state, action))
        if v < worst_value:
            worst_value = v
            worst_action = action
    return worst_action


def simulate(
    algorithm: str,
    start: tuple[int, ...],
    depth: int,
    max_solver_steps: int,
    seed: int = 7,
) -> TrialResult:
    rng = random.Random(seed)
    counter = NodeCounter()
    state = start
    trace: list[str] = []

    t0 = perf_counter()

    for _ in range(max_solver_steps):
        if is_goal(state):
            break

        if algorithm == "Minimax":
            solver_action = minimax_decision(state, depth, counter)
        elif algorithm == "AlphaBeta":
            solver_action = alphabeta_decision(state, depth, counter)
        elif algorithm == "Expectimax":
            solver_action = expectimax_decision(state, depth, counter)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        state = apply_action(state, solver_action)
        trace.append("S:" + solver_action)

        if is_goal(state):
            break

        # Environment step: adversary for Minimax/AlphaBeta, random for Expectimax.
        env_actions = legal_actions(state)
        if algorithm in ("Minimax", "AlphaBeta"):
            env_action = worst_disturbance_action(state)
        else:
            env_action = rng.choice(env_actions)

        state = apply_action(state, env_action)
        trace.append("E:" + env_action)

    elapsed = perf_counter() - t0
    return TrialResult(
        algorithm=algorithm,
        case_name="",
        solved=is_goal(state),
        steps=len(trace),
        elapsed_seconds=elapsed,
        expanded_nodes=counter.count,
        action_trace=" ".join(trace),
    )


def run_all() -> list[TrialResult]:
    cases = {
        "Case-A": (1, 2, 3, 4, 5, 6, 0, 7, 8),
        "Case-B": (1, 2, 3, 5, 0, 6, 4, 7, 8),
        "Case-C": (1, 3, 6, 5, 0, 2, 4, 7, 8),
    }

    algorithms = ["Minimax", "AlphaBeta", "Expectimax"]
    results: list[TrialResult] = []

    for case_name, start in cases.items():
        for algo in algorithms:
            r = simulate(algo, start, depth=4, max_solver_steps=24, seed=7)
            r.case_name = case_name
            results.append(r)

    return results


def write_report(path: str, results: list[TrialResult]) -> None:
    lines: list[str] = []
    lines.append("# 八数码对抗搜索补充实验报告（Minimax / Alpha-Beta / Expectimax）")
    lines.append("")
    lines.append("## 实验说明")
    lines.append("本实验为课程扩展：将八数码构造为两智能体博弈。求解者(S)希望接近目标状态，环境扰动者(E)在每回合对状态进行不利或随机扰动。")
    lines.append("")
    lines.append("- Minimax: E 取最坏动作")
    lines.append("- Alpha-Beta: 与 Minimax 同目标，使用剪枝")
    lines.append("- Expectimax: E 视为随机动作")
    lines.append("")
    lines.append("## 结果")
    lines.append("")
    lines.append("| Case | Algorithm | Solved | Trace Steps | Expanded Nodes | Time (s) | Action Trace |")
    lines.append("|---|---|---:|---:|---:|---:|---|")

    for r in results:
        lines.append(
            f"| {r.case_name} | {r.algorithm} | {r.solved} | {r.steps} | {r.expanded_nodes} | {r.elapsed_seconds:.6f} | {r.action_trace} |"
        )

    lines.append("")
    lines.append("## 分析")
    lines.append("- Alpha-Beta 与 Minimax 的决策质量相同，但通常扩展节点更少。")
    lines.append("- Expectimax 在随机扰动下更偏向平均表现，遇到强对抗环境时可能不如 Minimax 稳健。")
    lines.append("- 该建模是扩展实验，区别于标准单智能体八数码。")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    results = run_all()

    print("Adversarial 8-puzzle results:")
    for r in results:
        print(
            f"{r.case_name:6} | {r.algorithm:10} | solved={r.solved:<5} | "
            f"steps={r.steps:<3} | expanded={r.expanded_nodes:<6} | "
            f"time={r.elapsed_seconds:.6f}s"
        )

    out = "eight_puzzle_lab/8puzzle_adversarial_report.md"
    write_report(out, results)
    print(f"Report written to: {out}")


if __name__ == "__main__":
    main()
