# 8 Puzzle 搜索算法实验作业完成报告

## 1. 背景

8 Puzzle 是经典状态空间搜索问题。目标是在 3x3 棋盘中通过移动空格（记作 0）将初始状态变为目标状态：

- 目标状态：
  1 2 3
  4 5 6
  7 8 0

该问题常用于验证无信息搜索与启发式搜索方法的有效性，并比较不同算法在解质量与计算开销上的差异。

## 2. 任务

根据你的要求，新增独立实验目录完成以下工作：

1. 每人至少设计 3 种搜索算法求解问题。
2. 在 8 Puzzle 问题上测试这些算法并输出解。
3. 对不同算法的表现进行比较与分析，重点关注：
   - 解质量（是否最优、路径长度）
   - 时间复杂度表现（运行时间、扩展节点数）

## 3. 补充实现

本次在新目录中实现了 4 种算法（满足至少 3 种要求）：

- BFS（广度优先搜索）
- IDS（迭代加深深度优先）
- A*（Manhattan 启发式）
- Greedy Best-First（Manhattan 启发式）

实现文件：
- eight_puzzle_lab/run_experiment.py

实现要点：

- 使用元组表示状态，如 (1,2,3,4,5,6,7,0,8)
- 提供可解性判定（逆序数 parity）
- 统一动作集合 U/D/L/R
- 记录每个算法指标：
  - 是否求解成功
  - 解路径（动作序列）
  - 路径长度
  - 扩展节点数
  - 生成节点数
  - 耗时
- 自动生成实验结果文档：eight_puzzle_lab/experiment_report.md

## 4. 实验设置

测试用例（均可解）：

- Case-1-Easy: (1,2,3,4,5,6,7,0,8)
- Case-2-Medium: (1,2,3,4,8,0,7,6,5)
- Case-3-Harder: (2,3,6,1,5,0,4,7,8)

执行命令：

- python eight_puzzle_lab/run_experiment.py

## 5. 实验结果

### 5.1 Case-1-Easy

- BFS: solved=True, depth=1, expanded=4, generated=8, time=0.000032s, path=R
- IDS: solved=True, depth=1, expanded=5, generated=4, time=0.000011s, path=R
- A*: solved=True, depth=1, expanded=2, generated=4, time=0.000080s, path=R
- Greedy: solved=True, depth=1, expanded=2, generated=4, time=0.000068s, path=R

### 5.2 Case-2-Medium

- BFS: solved=True, depth=5, expanded=47, generated=76, time=0.000092s, path=DLURD
- IDS: solved=True, depth=5, expanded=95, generated=90, time=0.000126s, path=DLURD
- A*: solved=True, depth=5, expanded=6, generated=12, time=0.000036s, path=DLURD
- Greedy: solved=True, depth=5, expanded=6, generated=12, time=0.000030s, path=DLURD

### 5.3 Case-3-Harder

- BFS: solved=True, depth=7, expanded=116, generated=207, time=0.000227s, path=ULLDDRR
- IDS: solved=True, depth=7, expanded=269, generated=262, time=0.000274s, path=ULLDDRR
- A*: solved=True, depth=7, expanded=8, generated=13, time=0.000043s, path=ULLDDRR
- Greedy: solved=True, depth=7, expanded=8, generated=13, time=0.000034s, path=ULLDDRR

## 6. 对比分析

### 6.1 解质量

- BFS、IDS、A* 在本组单位代价问题上都得到最短路径。
- Greedy 在本次样例中也得到同样路径长度，但理论上不保证最优。

### 6.2 时间复杂度与搜索开销（经验结果）

- A* 在中高难度样例中扩展节点显著少于 BFS 和 IDS，表现最稳定。
- BFS 保证最优但扩展节点增长快，空间开销较高。
- IDS 空间优势明显，但因重复加深导致重复扩展，时间上通常慢于 A*。
- Greedy 往往较快，但可能被局部启发误导，难例中可能出现非最优解。

### 6.3 结论

- 若目标是最优解与较好效率平衡：A*（Manhattan）最推荐。
- 若强调实现简单且保证最优：BFS 可用，但规模增大时成本明显上升。
- 若内存受限：IDS 有实用价值。
- 若追求速度且可接受非最优：Greedy 可作为近似方案。

## 7. 任务完成情况

- 已新建独立实验目录并实现搜索实验。
- 已实现 4 种算法（超过至少 3 种的要求）。
- 已在 8 Puzzle 上完成测试并输出解路径。
- 已完成不同算法在解质量与时间复杂度方面的比较分析。

结论：本次新增任务已完成。