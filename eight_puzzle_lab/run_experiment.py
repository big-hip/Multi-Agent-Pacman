from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from time import perf_counter
from typing import Callable

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVES = {
    "U": -3,
    "D": 3,
    "L": -1,
    "R": 1,
}


@dataclass
class SearchResult:
    algorithm: str
    solved: bool
    path: list[str]
    expanded_nodes: int
    generated_nodes: int
    elapsed_seconds: float


def is_solvable(state: tuple[int, ...]) -> bool:
    nums = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                inversions += 1
    return inversions % 2 == 0


def manhattan(state: tuple[int, ...]) -> int:
    dist = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        goal_idx = val - 1
        dist += abs(idx // 3 - goal_idx // 3) + abs(idx % 3 - goal_idx % 3)
    return dist


def valid_move(blank_idx: int, action: str) -> bool:
    if action == "U":
        return blank_idx >= 3
    if action == "D":
        return blank_idx <= 5
    if action == "L":
        return blank_idx % 3 != 0
    if action == "R":
        return blank_idx % 3 != 2
    return False


def neighbors(state: tuple[int, ...]) -> list[tuple[str, tuple[int, ...]]]:
    out = []
    blank = state.index(0)
    for action in ("U", "D", "L", "R"):
        if not valid_move(blank, action):
            continue
        swap_idx = blank + MOVES[action]
        s = list(state)
        s[blank], s[swap_idx] = s[swap_idx], s[blank]
        out.append((action, tuple(s)))
    return out


def reconstruct_path(
    parents: dict[tuple[int, ...], tuple[tuple[int, ...] | None, str | None]],
    end_state: tuple[int, ...],
) -> list[str]:
    path: list[str] = []
    cur = end_state
    while True:
        prev, action = parents[cur]
        if prev is None or action is None:
            break
        path.append(action)
        cur = prev
    path.reverse()
    return path


def run_bfs(start: tuple[int, ...]) -> SearchResult:
    t0 = perf_counter()
    frontier = deque([start])
    visited = {start}
    parents = {start: (None, None)}
    expanded = 0
    generated = 1

    while frontier:
        cur = frontier.popleft()
        expanded += 1
        if cur == GOAL_STATE:
            return SearchResult(
                algorithm="BFS",
                solved=True,
                path=reconstruct_path(parents, cur),
                expanded_nodes=expanded,
                generated_nodes=generated,
                elapsed_seconds=perf_counter() - t0,
            )

        for action, nxt in neighbors(cur):
            if nxt in visited:
                continue
            visited.add(nxt)
            parents[nxt] = (cur, action)
            frontier.append(nxt)
            generated += 1

    return SearchResult("BFS", False, [], expanded, generated, perf_counter() - t0)


def _dls(
    state: tuple[int, ...],
    depth_left: int,
    path_states: set[tuple[int, ...]],
    expanded_counter: list[int],
    generated_counter: list[int],
) -> list[str] | None:
    expanded_counter[0] += 1
    if state == GOAL_STATE:
        return []
    if depth_left == 0:
        return None

    for action, nxt in neighbors(state):
        if nxt in path_states:
            continue
        generated_counter[0] += 1
        path_states.add(nxt)
        sub = _dls(nxt, depth_left - 1, path_states, expanded_counter, generated_counter)
        path_states.remove(nxt)
        if sub is not None:
            return [action] + sub
    return None


def run_ids(start: tuple[int, ...], max_depth: int = 40) -> SearchResult:
    t0 = perf_counter()
    total_expanded = 0
    total_generated = 1

    if start == GOAL_STATE:
        return SearchResult("IDS", True, [], 1, 1, perf_counter() - t0)

    for limit in range(max_depth + 1):
        expanded_counter = [0]
        generated_counter = [0]
        path_states = {start}
        path = _dls(start, limit, path_states, expanded_counter, generated_counter)
        total_expanded += expanded_counter[0]
        total_generated += generated_counter[0]
        if path is not None:
            return SearchResult(
                algorithm="IDS",
                solved=True,
                path=path,
                expanded_nodes=total_expanded,
                generated_nodes=total_generated,
                elapsed_seconds=perf_counter() - t0,
            )

    return SearchResult("IDS", False, [], total_expanded, total_generated, perf_counter() - t0)


def run_astar(start: tuple[int, ...]) -> SearchResult:
    t0 = perf_counter()
    pq: list[tuple[int, int, tuple[int, ...]]] = []
    parents = {start: (None, None)}
    g_cost = {start: 0}
    expanded = 0
    generated = 1
    tie = 0

    heappush(pq, (manhattan(start), tie, start))

    while pq:
        _, _, cur = heappop(pq)
        expanded += 1

        if cur == GOAL_STATE:
            return SearchResult(
                algorithm="A*_Manhattan",
                solved=True,
                path=reconstruct_path(parents, cur),
                expanded_nodes=expanded,
                generated_nodes=generated,
                elapsed_seconds=perf_counter() - t0,
            )

        cur_g = g_cost[cur]
        for action, nxt in neighbors(cur):
            nxt_g = cur_g + 1
            if nxt not in g_cost or nxt_g < g_cost[nxt]:
                g_cost[nxt] = nxt_g
                parents[nxt] = (cur, action)
                tie += 1
                heappush(pq, (nxt_g + manhattan(nxt), tie, nxt))
                generated += 1

    return SearchResult("A*_Manhattan", False, [], expanded, generated, perf_counter() - t0)


def run_greedy(start: tuple[int, ...]) -> SearchResult:
    t0 = perf_counter()
    pq: list[tuple[int, int, tuple[int, ...]]] = []
    parents = {start: (None, None)}
    visited = {start}
    expanded = 0
    generated = 1
    tie = 0

    heappush(pq, (manhattan(start), tie, start))

    while pq:
        _, _, cur = heappop(pq)
        expanded += 1

        if cur == GOAL_STATE:
            return SearchResult(
                algorithm="Greedy_Best_First",
                solved=True,
                path=reconstruct_path(parents, cur),
                expanded_nodes=expanded,
                generated_nodes=generated,
                elapsed_seconds=perf_counter() - t0,
            )

        for action, nxt in neighbors(cur):
            if nxt in visited:
                continue
            visited.add(nxt)
            parents[nxt] = (cur, action)
            tie += 1
            heappush(pq, (manhattan(nxt), tie, nxt))
            generated += 1

    return SearchResult("Greedy_Best_First", False, [], expanded, generated, perf_counter() - t0)


def format_board(state: tuple[int, ...]) -> str:
    rows = [state[i : i + 3] for i in range(0, 9, 3)]
    lines = []
    for row in rows:
        lines.append(" ".join(str(x) if x != 0 else "_" for x in row))
    return "\n".join(lines)


def run_suite() -> dict[str, list[SearchResult]]:
    test_cases = {
        "Case-1-Easy": (1, 2, 3, 4, 5, 6, 7, 0, 8),
        "Case-2-Medium": (1, 2, 3, 4, 8, 0, 7, 6, 5),
        "Case-3-Harder": (2, 3, 6, 1, 5, 0, 4, 7, 8),
    }

    algorithms: list[Callable[[tuple[int, ...]], SearchResult]] = [
        run_bfs,
        run_ids,
        run_astar,
        run_greedy,
    ]

    all_results: dict[str, list[SearchResult]] = {}

    for name, state in test_cases.items():
        if not is_solvable(state):
            raise ValueError(f"Unsolvable test case: {name}")

        case_results = []
        for algo in algorithms:
            case_results.append(algo(state))
        all_results[name] = case_results

    return all_results


def write_report(path: str, results: dict[str, list[SearchResult]]) -> None:
    lines: list[str] = []
    lines.append("# 8-Puzzle Search Experiment Report")
    lines.append("")
    lines.append("## Background")
    lines.append("This experiment evaluates multiple search strategies on the 8-puzzle problem. The objective is to compare solution quality and empirical time complexity using the same test instances.")
    lines.append("")
    lines.append("## Tasks")
    lines.append("- Implement at least 3 search algorithms.")
    lines.append("- Test algorithms on 8-puzzle instances and output solutions.")
    lines.append("- Compare solution quality and time complexity.")
    lines.append("")
    lines.append("## Implemented Algorithms")
    lines.append("- BFS")
    lines.append("- IDS (Iterative Deepening DFS)")
    lines.append("- A* (Manhattan Heuristic)")
    lines.append("- Greedy Best-First (Manhattan Heuristic)")
    lines.append("")
    lines.append("## Test Results")
    lines.append("")

    for case_name, case_results in results.items():
        lines.append(f"### {case_name}")
        lines.append("")
        lines.append("| Algorithm | Solved | Path Length | Expanded | Generated | Time (s) | Path |")
        lines.append("|---|---:|---:|---:|---:|---:|---|")
        for r in case_results:
            path_text = "".join(r.path) if r.path else "(empty)"
            lines.append(
                f"| {r.algorithm} | {str(r.solved)} | {len(r.path)} | {r.expanded_nodes} | {r.generated_nodes} | {r.elapsed_seconds:.6f} | {path_text} |"
            )
        lines.append("")

    lines.append("## Analysis")
    lines.append("- Solution quality: BFS/IDS/A* consistently return shortest paths on these unit-cost instances. Greedy may return longer paths in general, even if some cases happen to match optimal depth.")
    lines.append("- Time complexity (empirical): A* expands far fewer nodes than BFS/IDS on harder cases due to informed heuristic guidance.")
    lines.append("- IDS can find optimal depth with low memory but often repeats expansions across depth limits.")
    lines.append("- Greedy is usually fast but not guaranteed optimal.")
    lines.append("")
    lines.append("## Complexity Discussion")
    lines.append("- BFS: Complete and optimal for unit step cost; worst-case time/space are exponential in depth.")
    lines.append("- IDS: Complete and optimal for unit step cost; time is exponential with repeated re-expansion, memory is linear in depth.")
    lines.append("- A*: Complete and optimal with admissible/consistent heuristic (Manhattan); practical performance is usually best among optimal methods.")
    lines.append("- Greedy Best-First: Not optimal; often explores fewer nodes but can be misled by local heuristic choices.")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main() -> None:
    test_cases = {
        "Case-1-Easy": (1, 2, 3, 4, 5, 6, 7, 0, 8),
        "Case-2-Medium": (1, 2, 3, 4, 8, 0, 7, 6, 5),
        "Case-3-Harder": (2, 3, 6, 1, 5, 0, 4, 7, 8),
    }

    print("8-puzzle test cases:")
    for name, s in test_cases.items():
        print(f"\n{name}\n{format_board(s)}")

    results = run_suite()

    print("\nSearch outputs:")
    for case_name, case_results in results.items():
        print(f"\n[{case_name}]")
        for r in case_results:
            path = "".join(r.path) if r.path else "(empty)"
            print(
                f"{r.algorithm:18} solved={r.solved:<5} depth={len(r.path):<3} "
                f"expanded={r.expanded_nodes:<7} generated={r.generated_nodes:<7} "
                f"time={r.elapsed_seconds:.6f}s path={path}"
            )

    out_file = "eight_puzzle_lab/experiment_report.md"
    write_report(out_file, results)
    print(f"\nReport written to: {out_file}")


if __name__ == "__main__":
    main()
