# CS188 Project 2 Multi-Agent Pacman

## 项目背景
本项目基于 UC Berkeley CS188（Introduction to AI）Project 2，研究在多智能体对抗环境中如何进行决策。环境中 Pacman 与多个 Ghost 轮流行动，核心挑战是：

- 在有限深度下做出高质量策略决策
- 在对抗与随机对手建模中权衡收益与风险
- 通过评测框架验证算法正确性与策略表现

## 我完成的实现
本仓库的核心实现集中在 [multiAgents.py](multiAgents.py)：

- Q1 Reflex Agent 评估函数（[multiAgents.py](multiAgents.py#L55)）
- Q2 Minimax（[multiAgents.py](multiAgents.py#L130)）
- Q3 Alpha-Beta Pruning（[multiAgents.py](multiAgents.py#L195)）
- Q4 Expectimax（[multiAgents.py](multiAgents.py#L251)）
- Q5 Better Evaluation Function（[multiAgents.py](multiAgents.py#L302)）

## 关键技术说明（摘要）

1. 评估函数特征工程
- 使用食物距离倒数作为吸引项，提高近距离动作分辨率
- 将 Ghost 风险按 scared 与非 scared 分开建模
- 对 STOP 动作加入惩罚，抑制无效停滞

2. 多智能体深度语义统一
- 仅在所有 Ghost 行动结束、轮回 Pacman 时 depth + 1
- 保证 Minimax / Alpha-Beta / Expectimax 的深度含义一致

3. 搜索算法实现要点
- Minimax：Pacman max，Ghost min
- Alpha-Beta：在保持最优决策一致性的前提下降低展开节点
- Expectimax：Ghost 按均匀随机策略，使用期望值回传

4. 综合评估函数
- 融合当前分数、剩余食物/胶囊数量、最近目标距离、Ghost 风险收益
- 目标是平衡生存安全、清图效率与得分能力

## 已执行结果（用于汇报）
- 自动评分总分：25/25
- Q1：4/4，Average Score 1276.0，Win Rate 10/10
- Q5：6/6，Average Score 1178.3，Win Rate 10/10
- ReflexAgent 在 testClassic 10 局：Win Rate 10/10，Average Score 542.6

详情见：
- [docs/执行输出详情.md](docs/执行输出详情.md)
- [docs/logs/autograder_full_utf8.log](docs/logs/autograder_full_utf8.log)
- [docs/logs/reflex_testClassic_10_utf8.log](docs/logs/reflex_testClassic_10_utf8.log)

## 运行方式

```powershell
python autograder.py -q q1
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
python autograder.py
```

补充测试：

```powershell
python pacman.py -p ReflexAgent -l testClassic -n 10 -q
```

## 文档结构
- 项目总览与快速入口： [README.md](README.md)
- 汇报正文（背景、实现、关键技术）： [docs/汇报材料总览.md](docs/汇报材料总览.md)
- 执行结果与日志索引： [docs/执行输出详情.md](docs/执行输出详情.md)
- 10 分钟答辩讲稿： [docs/答辩讲稿_10分钟.md](docs/答辩讲稿_10分钟.md)
- 原始文档归档： [docs/archive](docs/archive)
