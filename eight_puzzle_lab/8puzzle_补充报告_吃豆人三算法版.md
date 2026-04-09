# 八数码补充实验报告（吃豆人三算法版）

## 1. 背景

课程主项目是 Pacman 多智能体搜索（Minimax、Alpha-Beta、Expectimax）。
为满足“每人至少 3 种搜索算法并在八数码上测试”的扩展要求，本补充实验将八数码重建为两智能体模型，复用上述三种对抗搜索方法进行实验。

说明：这属于“扩展建模”而非标准单智能体八数码。

## 2. 任务

- 使用 3 种算法：Minimax、Alpha-Beta、Expectimax
- 在八数码上测试并输出求解结果
- 对比分析解质量和时间复杂度（经验指标：求解成功率、节点扩展、耗时）

## 3. 建模与补充实现

实现文件：
- eight_puzzle_lab/adversarial_8puzzle_experiment.py

建模方式：

1. 求解者(Solver)回合：
   - 选择空格移动动作，目标是最大化状态评估值（接近目标状态）。
2. 环境(Env)回合：
   - Minimax / Alpha-Beta：环境选择最不利动作；
   - Expectimax：环境按随机动作分布采样。
3. 评估函数：
   - 以 Manhattan 距离 + 错位块数构成启发式；
   - 目标状态给予高奖励。

关键指标：
- solved（是否在步数上限内达到目标）
- steps（动作轨迹长度）
- expanded_nodes（搜索展开节点）
- elapsed_seconds（运行时间）

## 4. 实验结果

实际运行输出如下：

- Case-A:
  - Minimax: solved=False, steps=48, expanded=8588, time=0.017375s
  - Alpha-Beta: solved=False, steps=48, expanded=3726, time=0.007555s
  - Expectimax: solved=True, steps=8, expanded=876, time=0.001805s

- Case-B:
  - Minimax: solved=False, steps=48, expanded=4952, time=0.010557s
  - Alpha-Beta: solved=False, steps=48, expanded=2654, time=0.005950s
  - Expectimax: solved=True, steps=8, expanded=1104, time=0.002239s

- Case-C:
  - Minimax: solved=False, steps=48, expanded=5000, time=0.011028s
  - Alpha-Beta: solved=False, steps=48, expanded=2717, time=0.007676s
  - Expectimax: solved=True, steps=14, expanded=2164, time=0.006140s

自动报告文件：
- eight_puzzle_lab/8puzzle_adversarial_report.md

## 5. 对比分析

1. 解质量
- 在本扩展模型下，Expectimax 在给定案例中达到目标；
- Minimax 与 Alpha-Beta 在“强对抗扰动 + 有限步数”条件下更保守，未在步数上限内完成。

2. 时间复杂度（经验）
- Alpha-Beta 与 Minimax 决策目标一致，但节点扩展显著更少，耗时更低；
- Expectimax 的表现受随机扰动影响，在本实验中效率较好。

3. 结论
- 该三算法可以用于“扩展版八数码（对抗/随机环境）”；
- 若按“标准八数码”课程定义，仍建议使用 BFS/IDS/A* 作为主提交。

## 6. 完成情况

- 已完成“吃豆人三算法版”八数码实验实现
- 已输出测试结果并生成报告
- 已完成性能对比分析
