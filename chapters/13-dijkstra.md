# 第 13 章 · Dijkstra：每次确定当前最近的点

[返回目录](../README.md) · [上一章](12-graphs-toposort.md) · [下一章](14-dsu-mst.md)

**先修知识：** 第 09、12 章；理解图、邻接表与队列。

**本章完成后：** 用小根堆处理非负权最短路，区分候选距离、过期记录和最终确定的距离。

**建议学习方式：** 分两次完成。第一次读推导并手算，第二次盖住代码独立实现、做题和复盘。复杂章节可增加课次，不必一次读完。

## 1. 从最少步数变成最小代价

给定 n 个点、m 条有向边和起点 s，求 s 到每个点的最短距离。不可达输出 -1。
输入 n、m、s，随后 m 行 u、v、w，表示 u→v 的代价为 w。
1≤n≤200000，0≤m≤200000，0≤w≤10^9；允许零权边、重边和自环。
输出一行 n 个整数，按点编号排列。

边数少不代表代价小。例如 1→2 代价 10，1→3 代价 1，3→2 代价 1，去 2 的最优路线经过两条边，总代价只有 2。
BFS 先到的路线按边数分层，无法直接解决这个问题。

## 2. 候选距离与松弛

dist[v] 记录“目前找到的从 s 到 v 的最好距离”，开始设为无穷，只有 dist[s]=0。
当已有到 u 的路线，沿边 u→v 可以得到候选 dist[u]+w。
若比 dist[v] 更小，就更新，这一步叫松弛。更新说明找到了更好路线，并不意味着 v 已经最终确定。

## 3. 用小根堆选当前最近的候选

priority_queue 默认最大值先出。本章用 `greater<pair<long long,int>>` 改为最小值先出，堆中存 `(候选距离,点编号)`。
pair 先比较 first，first 相等再比较 second；这里点编号只用于打破平局。
每次距离变小就把新记录加入堆，旧记录无需立即删除。
弹出 `(d,u)` 时若 d!=dist[u]，说明它已被更好的记录替代，直接跳过。

## 4. 跟踪候选变化

使用 1→2(10)、1→3(1)、3→2(1)，起点 1：

| 有效弹出 | 松弛后距离 (1,2,3) | 堆中的重要记录 |
|---|---|---|
| (0,1) | (0,10,1) | (1,3)、(10,2) |
| (1,3) | (0,2,1) | (2,2)、(10,2) |
| (2,2) | (0,2,1) | (10,2) |
| (10,2) 过期 | 不变 | 空 |

代码中的“过期检查”发生在扫描出边之前，避免同一个点的旧距离重复触发昂贵遍历。

## 5. 为什么非负权允许最近点先确定

设 u 是当前候选距离最小的未确定点。如果存在一条更短的 s→u 路径，沿该路径找到第一个未确定点 x，其前驱已确定。
处理前驱时已经为 x 提供了不大于该路径前缀长度的候选距离。由于后续边权非负，这个前缀不超过整条短路长度，因而 dist[x]<dist[u]，与 u 最小矛盾。
因此 u 的当前距离就是最短距离。负权边会破坏“前缀不大于整条路径”的关键一步，所以本算法不用于含负权的图。

## 6. 数值与复杂度

在本题范围内最短简单路径长度小于 2×10^14，long long 足够。INF 选为 long long 最大值的四分之一，且不从无穷距离出发相加。
延迟删除版本至多因成功松弛产生 O(m+1) 条堆记录，时间 O(n+m+(m+1)log(m+2))，空间 O(n+m)。简单图中常写为 O((n+m)log n)。
不能把无穷直接输出成很大的数；题目约定不可达输出 -1。

## 完整 C++17 例题程序

独立源文件：[13-dijkstra.cpp](../examples/13-dijkstra.cpp)。输入输出约定见本章题目；程序针对题目保证的合法输入。

```cpp
#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, source;
    if (!(cin >> n >> m >> source)) return 0;
    vector<vector<pair<int, long long>>> graph(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v;
        long long weight;
        cin >> u >> v >> weight;
        graph[u].push_back({v, weight});
    }
    const long long INF = numeric_limits<long long>::max() / 4;
    vector<long long> dist(n + 1, INF);
    using State = pair<long long, int>;
    priority_queue<State, vector<State>, greater<State>> heap;
    dist[source] = 0;
    heap.push({0, source});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d != dist[u]) continue;  // 跳过旧记录
        for (auto [v, weight] : graph[u]) {
            if (d + weight < dist[v]) {
                dist[v] = d + weight;
                heap.push({dist[v], v});
            }
        }
    }
    for (int u = 1; u <= n; ++u) {
        if (u > 1) cout << ' ';
        cout << (dist[u] == INF ? -1 : dist[u]);
    }
    cout << '\n';
}
```

### 样例输入

```text
4 3 1
1 2 10
1 3 1
3 2 1
```

### 样例输出

```text
0 2 1 -1
```

## 分层练习：先独立做，再展开答案

1. 在样例中增加 2→4(0)，输出如何改变？
2. 为什么不能在第一次把点放入堆时，就宣布它的距离已经最优？
3. 若所有边权都是 1，用 BFS 和 Dijkstra 哪个更合适？

<details>
<summary>参考答案与思路（先尝试再看）</summary>

1. `0 2 1 2`。零权边合法，最短距离可以相同。
2. 点 2 第一次以距离 10 入堆，后来经 3 改为 2。要区分“发现候选”与“以最小有效距离弹出”。
3. BFS 即可，O(n+m)，不需要堆的额外对数开销。Dijkstra 仍正确，但没有利用等权这一更强条件。

</details>

## 过关标准

能解释松弛、过期检查和非负权前提；能手算同一个点被多次入堆的过程。

完成后在 [学习记录](../PROGRESS.md) 填写实际证据。看懂讲义、通过自带样例和独立掌握是三个不同阶段。

## 对照阅读

以下页面用于查阅术语与扩展。本文推导、示例与练习为独立编写，不是对 OI Wiki 原文的整页转载。

- [OI Wiki：最短路](https://oi-wiki.org/graph/shortest-path/)
- [OI Wiki：容器适配器](https://oi-wiki.org/lang/csl/container-adapter/)

[上一章](12-graphs-toposort.md) · [返回目录](../README.md) · [下一章](14-dsu-mst.md)
