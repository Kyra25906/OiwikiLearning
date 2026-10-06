# 第 15 章 · 树状数组：让前缀和支持动态修改

[返回目录](../README.md) · [上一章](14-dsu-mst.md) · [下一章](16-number-theory.md)

**先修知识：** 第 05 章；会数组和二进制的基本表示。

**本章完成后：** 掌握单点增加、区间求和的动态维护，并解释 lowbit 对应的区间。

**建议学习方式：** 分两次完成。第一次读推导并手算，第二次盖住代码独立实现、做题和复盘。复杂章节可增加课次，不必一次读完。

## 1. 前缀和遇到在线修改

给出 n 个数，接着 q 个操作：`1 i delta` 表示 a[i] 增加 delta；`2 l r` 查询当前闭区间 [l,r] 的和。
输入 n、q、数组和操作；1≤n≤200000，0≤q≤200000，下标从 1 开始，所有操作合法。
初值、增量绝对值≤10^9。修改和查询可以任意交错，因此第 05 章“全部更新后再还原”的方案不适用。

普通前缀和查询 O(1)，但 a[i] 改变后，i 及之后的前缀都要更新，最坏 O(n)。
我们想保存一些不同大小的区间，使一次修改只影响少量区间，而任意前缀又能由少量区间拼成。

## 2. lowbit 表示最低位的那个 1

正整数 x 的二进制最低有效 1 所代表的值叫 lowbit(x)，可用 `x & -x` 计算。
例如 12 的二进制为 1100，最低位 1 对应 0100，即 4；10=1010 的 lowbit 为 2。
`&` 是按位与：只有两边对应位都是 1，结果该位才为 1。这里的 & 不是第 01 章声明引用时的 &，语境不同。
在本程序正整数下标范围内，`x & -x` 的标准位运算技巧取出最低的 1；不要把对负值的一般移位假设混入其中。

## 3. bit[i] 究竟保存什么

定义 bit[i] 保存区间 `[i-lowbit(i)+1, i]` 的和。

| i | lowbit(i) | 保存的闭区间 |
|---:|---:|---|
| 1 | 1 | [1,1] |
| 2 | 2 | [1,2] |
| 3 | 1 | [3,3] |
| 4 | 4 | [1,4] |
| 6 | 2 | [5,6] |
| 8 | 8 | [1,8] |

例如查询前 6 项：先取 bit[6] 的 [5,6]，然后令 i=6-2=4，再取 bit[4] 的 [1,4]，最后到 0。
这些区间首尾相接、不重不漏，正好覆盖 [1,6]。

## 4. 修改沿着覆盖自己的大区间传播

给 a[3] 加 delta，会影响 bit[3]、bit[4]、bit[8]……。
下一个需要更新的下标是 `i+lowbit(i)`，它对应包含当前区间的下一个相关大区间。
查询通过减去 lowbit 拆前缀，修改通过加上 lowbit 向上扩展；二者方向相反。

对 `[1,2,3,4,5,6]`，查询 [2,5] 得 14；将 a[3] 加 10 后，数组变成 `[1,2,13,4,5,6]`，再查 [2,5] 得 24。
区间查询仍使用 prefix(r)-prefix(l-1)，变化的是 prefix 不再直接存在一张静态数组里，而是临时由若干 bit 区间相加。

## 5. 正确性与复杂度

初始化和每次单点更新都把增量加到所有覆盖该位置的相关 bit 区间，因此 bit 的区间定义始终成立。
查询按不相交区间分解前缀，所以求和正确。
每次查询去掉一个最低位 1，更新也逐步走向更大的二进制区间，均为 O(log n)。
本例逐个 add 建树需要 O(n log n)，q 次操作 O(q log n)，空间 O(n)。存在 O(n) 建树方法，但不是本章必需内容。

## 6. 边界与语义

add 的下标必须≥1，若从 0 开始，lowbit(0)=0，循环无法前进。prefix(0)=0 则是合法的。
本接口是“增加 delta”，不是“赋值为 delta”；若要赋新值，应先求新旧之差再增加。
树状数组不是任意区间操作都能直接处理；本章承诺的能力仅是单点加、区间和。

## 完整 C++17 例题程序

独立源文件：[15-fenwick.cpp](../examples/15-fenwick.cpp)。输入输出约定见本章题目；程序针对题目保证的合法输入。

```cpp
#include <iostream>
#include <vector>
using namespace std;

struct Fenwick {
    int n;
    vector<long long> bit;
    explicit Fenwick(int length) : n(length), bit(length + 1, 0) {}
    void add(int i, long long delta) {
        for (; i <= n; i += i & -i) bit[i] += delta;
    }
    long long prefix(int i) const {
        long long result = 0;
        for (; i > 0; i -= i & -i) result += bit[i];
        return result;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    Fenwick tree(n);
    for (int i = 1; i <= n; ++i) {
        long long x;
        cin >> x;
        tree.add(i, x);
    }
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int i;
            long long delta;
            cin >> i >> delta;
            tree.add(i, delta);
        } else {
            int l, r;
            cin >> l >> r;
            cout << tree.prefix(r) - tree.prefix(l - 1) << '\n';
        }
    }
}
```

### 样例输入

```text
6 3
1 2 3 4 5 6
2 2 5
1 3 10
2 2 5
```

### 样例输出

```text
14
24
```

## 分层练习：先独立做，再展开答案

1. 查询 prefix(7) 会依次访问哪些 bit 下标？分别覆盖什么区间？
2. n=8 时，给 a[5] 增加 2，会修改哪些 bit 下标？
3. 如何将本接口包装成“把 a[i] 赋值为 v”？

<details>
<summary>参考答案与思路（先尝试再看）</summary>

1. 7、6、4，区间分别为 [7,7]、[5,6]、[1,4]。
2. 5、6、8。增量会分别进入 [5,5]、[5,6]、[1,8]。
3. 额外保存原数组，执行 add(i,v-a[i])，然后令 a[i]=v；也可通过 prefix(i)-prefix(i-1) 查询旧值。直接 add(i,v) 会变成累加而非赋值。

</details>

## 过关标准

能手画 bit 所覆盖的区间；能解释两个 lowbit 循环，并正确处理 1-based 下标。

完成后在 [学习记录](../PROGRESS.md) 填写实际证据。看懂讲义、通过自带样例和独立掌握是三个不同阶段。

## 对照阅读

以下页面用于查阅术语与扩展。本文推导、示例与练习为独立编写，不是对 OI Wiki 原文的整页转载。

- [OI Wiki：树状数组](https://oi-wiki.org/ds/fenwick/)
- [OI Wiki：位运算](https://oi-wiki.org/math/bit/)

[上一章](14-dsu-mst.md) · [返回目录](../README.md) · [下一章](16-number-theory.md)
