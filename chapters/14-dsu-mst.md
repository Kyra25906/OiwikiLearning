# 第 14 章 · 并查集与最小生成树：便宜地连接所有点

[返回目录](../README.md) · [上一章](13-dijkstra.md) · [下一章](15-fenwick.md)

**先修知识：** 第 04、12 章；会函数与 struct。

**本章完成后：** 用并查集维护连通块，理解 Kruskal 的选边条件与最优性。

**建议学习方式：** 分两次完成。第一次读推导并手算，第二次盖住代码独立实现、做题和复盘。复杂章节可增加课次，不必一次读完。

## 1. 先区分两种图问题

输入一个无向带权图，选择若干条边，使所有 n 个点连通且总费用最小。
输入 n、m，随后 m 行 u、v、w；1≤n≤200000，0≤m≤200000，权重绝对值≤10^9。
允许重边、自环和负权。要求输出最小生成树的权值和；无法连通输出 IMPOSSIBLE。
准确地说，本题选择的是一棵生成树，即连通且无环、恰含 n-1 条边；负权存在时不能把题意改成“任意连通子图”。

最短路最小化某个起点到其他点的路径代价，最小生成树最小化所选整棵树的边权总和，这两个目标不同。

## 2. 什么信息能判断加边会不会成环

若 u、v 已经连通，再加 u-v 就形成环；若不连通，加边就把两个连通块合成一个。
并查集给每个连通块维护一个代表。find(x) 找代表，merge(a,b) 合并代表不同的两个集合。
初始每个点单独成块，parent[x]=x。

find 不需要整块扫描，只沿 parent 指针走到根。路径压缩会让沿途节点更接近根，减少后续查找。
合并时把较小集合的根接到较大集合的根，叫按大小合并。size 只在根节点上有含义。
代码使用迭代的路径减半，不依赖深递归。

代码里的 `explicit DSU(int n)` 是构造函数，在执行 `DSU dsu(n)` 时建立这份并查集。
冒号后的 `parent(n+1), size(n+1,1)` 是成员初始化：前者创建父节点数组，后者把各集合大小先设为 1。
`iota(parent.begin(), parent.end(), 0)` 再依次填入 0、1、2……，建立每个节点指向自己的初始状态。
`explicit` 禁止把一个整数悄悄转换为 DSU 对象，不影响这里显式创建对象的写法。

## 3. Kruskal 的完整步骤

把所有边按权重从小到大排序。逐条检查：两端不连通就选它并合并，已经连通就跳过。
直到选出 n-1 条边，得到生成树。若边看完仍不足 n-1 条，图不连通。
自环两端代表相同，自然被跳过；重复边也会通过连通判断处理。

## 4. 跟踪连通块合并

边为 1-2(1)、2-3(2)、1-3(3)、3-4(4)：

| 检查边 | 是否选 | 连通块 | 累计费用 |
|---|---|---|---:|
| 1-2(1) | 选 | {1,2},{3},{4} | 1 |
| 2-3(2) | 选 | {1,2,3},{4} | 3 |
| 1-3(3) | 跳过，会成环 | 不变 | 3 |
| 3-4(4) | 选 | {1,2,3,4} | 7 |

并查集代表只用于判断属于哪一块，不必等于块中最小编号，也不直接保存生成树上的路径。

## 5. 为什么贪心选边安全

假设已经选的边能被某棵最小生成树包含。现在选一条连接两个当前连通块的最便宜可选边 e。
若该最小生成树已有 e，无需改变；否则把 e 加入树会形成一个环。环上一定还有一条边 f 跨过 e 所连接的某个当前连通块的边界。
这条 f 不是已经选中的块内边，而且其权重不会小于当前按升序选到的 e。
用 e 替换 f，仍是一棵树，总费用不增加，并包含新选择。因此可一步步保持“存在兼容当前选择的最优树”。

## 6. 代价与边界

并查集结合两种优化，单次操作摊还 O(α(n))，α 增长极慢；不是严格常数。
Kruskal 总时间 O(n+m log(m+1)+mα(n))，空间 O(n+m)，主要成本通常是排序。
n=1 时不用任何边，答案 0；负权不会破坏按权重排序和交换论证。

## 完整 C++17 例题程序

独立源文件：[14-dsu-mst.cpp](../examples/14-dsu-mst.cpp)。输入输出约定见本章题目；程序针对题目保证的合法输入。

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

struct DSU {
    vector<int> parent, size;
    explicit DSU(int n) : parent(n + 1), size(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        while (x != parent[x]) {
            parent[x] = parent[parent[x]];  // 路径减半
            x = parent[x];
        }
        return x;
    }
    bool merge(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (size[a] < size[b]) swap(a, b);
        parent[b] = a;
        size[a] += size[b];
        return true;
    }
};
struct Edge { int u, v; long long weight; };

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<Edge> edges(m);
    for (auto &e : edges) cin >> e.u >> e.v >> e.weight;
    sort(edges.begin(), edges.end(), [](const Edge &a, const Edge &b) {
        return a.weight < b.weight;
    });
    DSU dsu(n);
    int used = 0;
    long long total = 0;
    for (const auto &e : edges) {
        if (dsu.merge(e.u, e.v)) {
            total += e.weight;
            ++used;
            if (used == n - 1) break;
        }
    }
    if (used == n - 1) cout << total << '\n';
    else cout << "IMPOSSIBLE\n";
}
```

### 样例输入

```text
4 4
1 2 1
2 3 2
1 3 3
3 4 4
```

### 样例输出

```text
7
```

## 分层练习：先独立做，再展开答案

1. n=3，只有边 1-2(1)，程序输出什么？
2. 三角形边权为 1、2、3，最小生成树总权值是多少？为什么不是三条都选？
3. 在 DSU 中增加“当前连通块数量”的统计，应该何时减少？

<details>
<summary>参考答案与思路（先尝试再看）</summary>

1. IMPOSSIBLE。点 3 与其他点不连通。
2. 3，取权重 1 与 2 的两条边。生成树要求无环；三条边构成环。
3. 初始为 n，仅当 merge 成功时减 1。同块内重复合并不能减少，因为并没有把两个不同集合变成一个。

</details>

## 过关标准

能手算 parent 与连通块变化；说明按大小合并与路径压缩；区分最短路树和最小生成树。

完成后在 [学习记录](../PROGRESS.md) 填写实际证据。看懂讲义、通过自带样例和独立掌握是三个不同阶段。

## 对照阅读

以下页面用于查阅术语与扩展。本文推导、示例与练习为独立编写，不是对 OI Wiki 原文的整页转载。

- [OI Wiki：并查集](https://oi-wiki.org/ds/dsu/)
- [OI Wiki：最小生成树](https://oi-wiki.org/graph/mst/)

[上一章](13-dijkstra.md) · [返回目录](../README.md) · [下一章](15-fenwick.md)
