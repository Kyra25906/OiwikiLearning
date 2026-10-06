# OiwikiLearning · 从直觉到独立解题

面向有 C/C++ 基础、希望系统学习算法的学习者。一套 **18 章中文讲义 + 18 个完整 C++17 例题 + 54 道分层练习及参考思路**，配套可调整的 **12 周学习计划**。

本仓库参考 [OI Wiki 的知识分类](https://oi-wiki.org/) 组织学习，采用独立编写的推导和例题；不是 OI Wiki 官方课程，也不承诺覆盖站内全部专题。首轮目标是建立基础解题能力，进阶专题见 [后续路线](STUDY_PLAN.md#首轮之后的拓展)。

## 从这里开始

1. 阅读 [学习计划与详细目录](STUDY_PLAN.md)，了解先修关系、每周安排和验收方式。
2. 从 [第 01 章](chapters/01-cpp-toolkit.md) 开始；已熟悉输入、vector 和数值范围的同学，可先做第 01 章练习，通过后进入 [第 02 章：枚举](chapters/02-enumeration-complexity.md)。
3. 每章按 **题意 → 朴素想法 → 改进依据 → 手算 → 完整代码 → 练习 → 复盘** 学习。先尝试练习，再展开答案。
4. 将实际学习情况记入 [进度与错题记录](PROGRESS.md)。章节文件齐全不代表你已学完，初始进度全部留空。

## 讲义目录

| 章 | 讲义 | 建议周次 | 可验证目标 |
|---|---|---|---|
| 01 | [C++17 起步：让数据在程序里流动](chapters/01-cpp-toolkit.md) | 1 | 独立读入一个数组，统计总和、最大值和最大值出现次数。 |
| 02 | [枚举与复杂度：不漏、不重、算得完](chapters/02-enumeration-complexity.md) | 1 | 把候选答案范围写清楚，证明枚举完整，并估计运算规模。 |
| 03 | [模拟：先定义状态，再落实规则](chapters/03-simulation.md) | 2 | 将自然语言规则变成逐步状态转移，并用轨迹表定位错误。 |
| 04 | [排序与贪心：为什么先结束的活动值得先选](chapters/04-sorting-greedy.md) | 2 | 会用 struct、sort 和比较函数，并用交换论证证明一次贪心选择。 |
| 05 | [前缀和与差分：复用区间里的重复工作](chapters/05-prefix-difference.md) | 3 | 完成先批量区间加、再批量区间求和的离线任务，解释两个前缀过程的含义。 |
| 06 | [二分查找：维护一个一定包含答案的范围](chapters/06-binary-search.md) | 3 | 独立实现 lower_bound，并用不变量解释每次丢弃半边的原因。 |
| 07 | [双指针：利用有序性批量排除候选](chapters/07-two-pointers.md) | 4 | 将两数之和计数从 O(n²) 改为 O(n log n)，并正确处理重复值。 |
| 08 | [递归与 DFS：沿着选择树走，再恢复现场](chapters/08-recursion-dfs.md) | 4 | 用深度优先搜索枚举子集，明确参数、终止条件和回溯恢复。 |
| 09 | [BFS：一层一层扩展最少步数](chapters/09-bfs.md) | 5 | 用队列求网格中的最少步数，理解首次到达为何最优。 |
| 10 | [动态规划入门：用状态保存已经解决的子问题](chapters/10-dp-basics.md) | 6 | 从枚举前驱推导最长严格递增子序列的状态、转移和顺序。 |
| 11 | [0/1 背包：同一个物品为什么不能重复拿](chapters/11-knapsack.md) | 6 | 从二维状态推导一维压缩，解释容量倒序的因果关系。 |
| 12 | [图的表示与拓扑排序：先完成依赖，再执行任务](chapters/12-graphs-toposort.md) | 7 | 建立有向图邻接表，用入度判断可执行任务，并检测依赖环。 |
| 13 | [Dijkstra：每次确定当前最近的点](chapters/13-dijkstra.md) | 8 | 用小根堆处理非负权最短路，区分候选距离、过期记录和最终确定的距离。 |
| 14 | [并查集与最小生成树：便宜地连接所有点](chapters/14-dsu-mst.md) | 8—9 | 用并查集维护连通块，理解 Kruskal 的选边条件与最优性。 |
| 15 | [树状数组：让前缀和支持动态修改](chapters/15-fenwick.md) | 9 | 掌握单点增加、区间求和的动态维护，并解释 lowbit 对应的区间。 |
| 16 | [数学基础：余数、最大公约数与快速幂](chapters/16-number-theory.md) | 10 | 理解欧几里得算法与二进制拆指数，并在规定范围内安全实现模幂。 |
| 17 | [字符串与 KMP：失配之后保留已经匹配的信息](chapters/17-kmp.md) | 11 | 推导前缀函数，理解失配跳转，并找出所有允许重叠的匹配位置。 |
| 18 | [综合训练：从题意选择方法，建立自己的验证闭环](chapters/18-integration.md) | 12 | 独立完成读题、建模、证明、复杂度估计、编码和反例验证。 |

## 如何运行例题

每个 examples 文件都是单独可编译的程序，不依赖其他章节。使用支持 C++17 的编译器。在仓库根目录打开终端，以第二章为例：

```powershell
New-Item -ItemType Directory -Force .build | Out-Null
g++ -std=c++17 -O2 -Wall -Wextra -pedantic examples/02-enumeration-complexity.cpp -o .build/pairs.exe
@"
4 5
2 2 3 3
"@ | .\.build\pairs.exe
```

输出应为 `4`。其他章节的输入格式与样例写在各自讲义里。无需为了阅读讲义安装 Python。

## 如何复查材料

若已安装 Python 3.10+ 和 g++，在根目录运行：

```text
python scripts/check.py
```

检查包括全部例题的 C++17 编译、讲义代码与独立源文件一致性、样例与边界测试、固定随机种子的小规模独立对拍、仓库内 Markdown 链接。
详细记录见 [验证说明](VALIDATION.md)。这是本地验证，不代表已向某个在线评测平台提交通过。
可用 `python scripts/check.py --cxx 编译器路径` 指定编译器；构建产物只放入被 Git 忽略的 `.build/`。

## 文件布局

```text
STUDY_PLAN.md       学习计划、顺序与后续路线
chapters/          18 章完整讲义，含折叠参考答案
examples/          每章一个独立 C++17 程序
tests/cases.json   样例和固定边界用例
scripts/check.py   编译、链接检查与独立小规模对拍
PROGRESS.md        学习与错题记录，供实际填写
SOURCES.md         OI Wiki 对照阅读入口及来源说明
VALIDATION.md      本次材料验证范围和结果
```

后续一起学习时，可以直接说“带我学第 05 章，先讲差分为什么只改边界”，我们便从一个可手算的小步骤继续。
