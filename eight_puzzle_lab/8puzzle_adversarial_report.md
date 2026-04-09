# 八数码对抗搜索补充实验报告（Minimax / Alpha-Beta / Expectimax）

## 实验说明
本实验为课程扩展：将八数码构造为两智能体博弈。求解者(S)希望接近目标状态，环境扰动者(E)在每回合对状态进行不利或随机扰动。

- Minimax: E 取最坏动作
- Alpha-Beta: 与 Minimax 同目标，使用剪枝
- Expectimax: E 视为随机动作

## 结果

| Case | Algorithm | Solved | Trace Steps | Expanded Nodes | Time (s) | Action Trace |
|---|---|---:|---:|---:|---:|---|
| Case-A | Minimax | False | 48 | 8588 | 0.017375 | S:R E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U |
| Case-A | AlphaBeta | False | 48 | 3726 | 0.007555 | S:R E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U |
| Case-A | Expectimax | True | 8 | 876 | 0.001805 | S:R E:L S:R E:U S:D E:L S:R E:R |
| Case-B | Minimax | False | 48 | 4952 | 0.010557 | S:L E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U |
| Case-B | AlphaBeta | False | 48 | 2654 | 0.005950 | S:L E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U |
| Case-B | Expectimax | True | 8 | 1104 | 0.002239 | S:L E:D S:R E:U S:D E:L S:R E:R |
| Case-C | Minimax | False | 48 | 5000 | 0.011028 | S:L E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U |
| Case-C | AlphaBeta | False | 48 | 2717 | 0.007676 | S:L E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U S:D E:U |
| Case-C | Expectimax | True | 14 | 2164 | 0.006140 | S:L E:D S:R E:U S:R E:D S:U E:L S:R E:U S:L E:D S:D E:R |

## 分析
- Alpha-Beta 与 Minimax 的决策质量相同，但通常扩展节点更少。
- Expectimax 在随机扰动下更偏向平均表现，遇到强对抗环境时可能不如 Minimax 稳健。
- 该建模是扩展实验，区别于标准单智能体八数码。