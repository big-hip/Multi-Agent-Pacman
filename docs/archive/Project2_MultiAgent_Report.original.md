# CS188 Project 2 多智能体搜索作业报告（最终版）

## 1. 项目概述

- 课程：UC Berkeley CS188 Introduction to AI
- 项目：Project 2 - Multi-Agent Search
- 目标：在 Pacman 对抗环境中实现并验证多智能体决策算法

本项目聚焦五个核心任务：

1. Q1：Reflex Agent 评估函数设计
2. Q2：Minimax 多智能体搜索
3. Q3：Alpha-Beta 剪枝优化
4. Q4：Expectimax 随机对手建模
5. Q5：Better Evaluation Function 综合启发式设计

## 2. 需求分析

项目要求不仅是“可运行”，还需要满足以下约束：

- 算法语义正确（多幽灵轮转、深度定义一致）
- 评测展开行为正确（尤其 Q2/Q3）
- 结果稳定（Q1/Q5 要达到分数与胜率门槛）
- 代码集中在学生文件，不改评分框架

## 3. 实现方案

实现集中在 multiAgents.py。

### 3.1 Q1 Reflex Agent

设计思路：基于后继状态分数，叠加启发式特征。

- 食物吸引：使用最近食物距离倒数，提高就近吃豆倾向
- 停止惩罚：抑制无效停留
- 幽灵风险控制：
  - 非 scared 幽灵：距离越近惩罚越大
  - scared 幽灵：距离越近奖励越大
  - 与危险幽灵重合：直接判定极差状态

### 3.2 Q2 Minimax

- Pacman 为 max 节点，幽灵为 min 节点
- 使用 agentIndex 循环处理多个幽灵
- 当轮转回 Pacman 时 depth + 1，满足 ply 语义
- 在胜/负/深度上限/无合法动作时回退评估函数

### 3.3 Q3 Alpha-Beta

- 在 Minimax 上增加 alpha 与 beta 边界
- 保持与 Minimax 一致的决策结果
- 在保证正确性的前提下降低搜索展开规模

### 3.4 Q4 Expectimax

- Pacman 仍最大化收益
- 幽灵层按均匀随机策略计算期望值
- 用于建模“对手非总是最坏动作”的情形

### 3.5 Q5 Better Evaluation

综合特征：

- 当前分数（基础项）
- 最近食物距离 + 食物数量惩罚
- 胶囊距离 + 胶囊数量惩罚
- 幽灵危险惩罚与 scared 追击奖励

目标是在“安全性、清图速度、收益”间取得平衡。

## 4. 实验方法

### 4.1 自动评分命令

```powershell
python autograder.py -q q1
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
```

### 4.2 补充运行命令

```powershell
python pacman.py -p ReflexAgent -l testClassic -n 10 -q
```

用于观察策略在固定布局下的稳定性（胜率、均分）。

## 5. 结果汇总

### 5.1 分题得分

| 题号 | 分数 |
|---|---|
| Q1 | 4/4 |
| Q2 | 5/5 |
| Q3 | 5/5 |
| Q4 | 5/5 |
| Q5 | 6/6 |

代码总分：25/25

### 5.2 关键性能指标

- Q1：Win Rate 10/10，Average Score 1276.0
- Q5：Win Rate 10/10，Average Score 1178.3

说明：结果满足并超过常见门槛，策略稳定性较好。

## 6. 问题与修正

1. 初版策略存在停滞动作偏多的问题：
   - 通过 STOP 惩罚缓解。
2. 早期评估函数风险收益耦合不清：
   - 将幽灵按 scared 与非 scared 分开建模。
3. 多智能体深度计数易错：
   - 统一采用“回到 Pacman 才加一层”的 ply 定义。

## 7. 结论

本项目已完整实现 CS188 Project 2 要求的五项核心算法与评估函数，自动评分全部通过。代码结构、评测结果与实验记录满足课程提交要求，可直接用于最终提交。

## 8. 提交检查

- multiAgents.py 为最终代码
- q1-q5 自动评分均通过
- 报告内容与实际运行结果一致
- 完成平台端 Q6 反思与声明填写
