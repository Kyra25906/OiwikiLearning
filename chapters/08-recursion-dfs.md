# 第 08 章 · 递归与 DFS：沿着选择树走，再恢复现场

[返回目录](../README.md) · [上一章](07-two-pointers.md) · [下一章](09-bfs.md)

**先修知识：** 第 01—03 章；会函数调用。

**本章完成后：** 用深度优先搜索枚举子集，明确参数、终止条件和回溯恢复。

**建议学习方式：** 分两次完成。第一次读推导并手算，第二次盖住代码独立实现、做题和复盘。复杂章节可增加课次，不必一次读完。

## 1. 每个位置都有选与不选两个分支

给出 n 个整数和 target，统计和等于 target 的子集数量。子集按位置区分，允许空集。
输入 n、target，接着 n 个数；0≤n≤20，数值绝对值≤10^9，target 绝对值≤2×10^10。
与两数之和不同，这里没有固定选几个数。直接写固定层数的 for 循环不方便，于是让函数代表“接下来继续做选择”。

## 2. 先说清楚函数的承诺

`dfs(pos,sum)` 的含义：前 pos 个位置已经决定选不选，已选元素之和为 sum；现在枚举剩余位置的所有选择。
当 pos==n，所有选择都完成了，此时检查 sum 是否等于 target。
否则，对当前位置产生两种互斥情况：不选，进入 dfs(pos+1,sum)；选，进入 dfs(pos+1,sum+a[pos])。
每次 pos 增大，最终一定到达 n，因此递归有明确终点。

## 3. 手动展开一棵小树

数组 `[1,2]`、target=2，根为 dfs(0,0)：

```text
dfs(0,0)
├─ 不选 1：dfs(1,0)
│  ├─ 不选 2：dfs(2,0) → 空集，和 0
│  └─ 选择 2：dfs(2,2) → {位置1}，计数 +1
└─ 选择 1：dfs(1,1)
   ├─ 不选 2：dfs(2,1) → {位置0}
   └─ 选择 2：dfs(2,3) → {位置0,位置1}
```

DFS 的执行顺序是先沿一条分支走到底，返回后再试同层的下一个分支。
“返回”不是清空整个程序，而是恢复到上一层函数调用继续执行。
每个位置的选/不选序列唯一对应一个子集，所以叶子不漏不重地覆盖所有子集。

## 4. 哪些状态需要恢复

pos、sum 是按值传递，每层有自己的副本，因此回来后不用手动减去 a[pos]。
代码额外保存 chosen，演示共享路径的回溯：选当前位置前 push_back，返回后 pop_back。
若忘记 pop_back，下一分支会继承上一分支遗留的选择，打印路径时就会错。
本例只输出计数，chosen 可删；保留它是为了展示以后输出方案时所需的机制。

## 5. 剪枝必须有前提

能否在 sum>target 时立即返回？本题不能，因为后面可能有负数把和拉回来。
例如 `[5,-4]`、target=1，选 5 后若立即剪枝，就会漏掉 {5,-4}。
只有能证明某个分支不可能产生答案，才可以删掉它。搜索顺序影响速度，错误的剪枝影响正确性。

## 6. 代价与递归边界

二叉选择树有 2^n 个叶子、2^(n+1)-1 个节点，总时间 O(2^n)，递归栈及路径 O(n)。
本题 n≤20 是因为指数增长，不是因为递归语法本身慢。
后面遍历很深的图时，递归深度可能达到数十万并耗尽调用栈，需要显式栈；本题深度只有 20。

## 完整 C++17 例题程序

独立源文件：[08-recursion-dfs.cpp](../examples/08-recursion-dfs.cpp)。输入输出约定见本章题目；程序针对题目保证的合法输入。

```cpp
#include <iostream>
#include <vector>
using namespace std;
vector<long long> a;
vector<int> chosen;
int n;
long long target, answer = 0;

void dfs(int pos, long long sum) {
    if (pos == n) {
        if (sum == target) ++answer;
        return;
    }
    dfs(pos + 1, sum);  // 不选当前位置
    chosen.push_back(pos);
    dfs(pos + 1, sum + a[pos]);
    chosen.pop_back();  // 共享路径必须恢复
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    if (!(cin >> n >> target)) return 0;
    a.resize(n);
    for (auto &x : a) cin >> x;
    dfs(0, 0);
    cout << answer << '\n';
}
```

### 样例输入

```text
3 3
1 2 3
```

### 样例输出

```text
2
```

## 分层练习：先独立做，再展开答案

1. `[0,0]`、target=0 有几个子集？把它们按位置写出来。
2. 在叶子处输出 chosen，修改程序列出所有满足条件的非空子集。
3. 如果所有数都非负，sum>target 时能否剪枝？sum==target 时能否直接返回？

<details>
<summary>参考答案与思路（先尝试再看）</summary>

1. 4 个：空集、{0}、{1}、{0,1}。值一样不代表选择一样。
2. 在 `pos==n && sum==target && !chosen.empty()` 时输出 chosen 的所有下标。push/pop 使它准确表示当前叶子的方案。
3. sum>target 可以剪，因为以后不会减小；sum==target 不能简单返回计数 1，因为后面可能有零，选或不选零会产生不同合法子集。

</details>

## 过关标准

能说清 dfs 参数含义、终止条件、分支覆盖与现场恢复，并举出错误剪枝反例。

完成后在 [学习记录](../PROGRESS.md) 填写实际证据。看懂讲义、通过自带样例和独立掌握是三个不同阶段。

## 对照阅读

以下页面用于查阅术语与扩展。本文推导、示例与练习为独立编写，不是对 OI Wiki 原文的整页转载。

- [OI Wiki：递归 & 分治](https://oi-wiki.org/basic/divide-and-conquer/)
- [OI Wiki：DFS（搜索）](https://oi-wiki.org/search/dfs/)
- [OI Wiki：回溯法](https://oi-wiki.org/search/backtracking/)

[上一章](07-two-pointers.md) · [返回目录](../README.md) · [下一章](09-bfs.md)
