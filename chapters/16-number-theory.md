# 第 16 章 · 数学基础：余数、最大公约数与快速幂

[返回目录](../README.md) · [上一章](15-fenwick.md) · [下一章](17-kmp.md)

**先修知识：** 第 02、08 章；会整数除法和余数。

**本章完成后：** 理解欧几里得算法与二进制拆指数，并在规定范围内安全实现模幂。

**建议学习方式：** 分两次完成。第一次读推导并手算，第二次盖住代码独立实现、做题和复盘。复杂章节可增加课次，不必一次读完。

## 1. 两个小任务共享一组输入

输入 a、b、p，第一行输出 gcd(a,b)，第二行输出 a^b mod p。
0≤a≤10^9，0≤b≤10^18，1≤p≤10^9。约定 gcd(0,0)=0，指数为 0 时幂取 1，包括本练习中的 0^0。
p=1 时所有整数对 p 的余数都为 0。
这份范围特意限制模数，使模乘的中间结果可以用 long long 保存。

## 2. 最大公约数为什么能用余数缩小

若 a=q*b+r，则一个数同时整除 a、b，当且仅当它同时整除 b、r。
一方面 d|a 且 d|b，则 d|(a-qb)=r；反方向 d|b 且 d|r，则 d|(qb+r)=a。
两组数的公约数完全相同，所以 gcd(a,b)=gcd(b,a%b)。
不断替换，第二个数严格变小，最后变成 0；此时 gcd(a,0)=a。

例如 gcd(48,18)：`(48,18)→(18,12)→(12,6)→(6,0)`，答案 6。
这是一种通过保持答案不变、不断缩小输入的算法。

## 3. 为什么不直接乘 b 次

b 可以达到 10^18，线性乘法不可行。观察 13=8+4+1，所以 a^13=a^8*a^4*a。
只要不断平方，就能依次得到 a、a²、a⁴、a⁸……；根据指数的二进制位决定是否把当前项乘入答案。
代码中 `exponent & 1` 检查最低位是否为 1，`exponent >>= 1` 对非负指数相当于除以 2 向下取整。

## 4. 跟踪 3^5 mod 7

初始化 result=1、base=3、exponent=5：

| 处理前 exponent | base | 本位是否乘入 | 处理后 result |
|---:|---:|---|---:|
| 5 | 3 | 是 | 3 |
| 2 | 2（3² mod 7） | 否 | 3 |
| 1 | 4（2² mod 7） | 是 | 5 |

下一轮指数为 0，结果 5。全过程只保留余数，不需要先算出巨大的原始幂。

## 5. 用不变量解释快速幂

始终保持 `result * base^exponent` 与最初 a^b 模 p 同余。
若 exponent 为奇数，先将一个 base 乘入 result；剩余指数为偶数，再将 base 平方、exponent 减半。
若 exponent 为偶数，直接平方底数、指数减半，乘积表示不变。
最终 exponent=0，剩下 result 就与目标同余。

## 6. 模运算的边界

每次乘法前两个因子都小于 p≤10^9，因此乘积小于 10^18，适合 long long。
若允许 p 接近 10^18，本程序的乘法可能溢出，需要更宽类型或专门模乘，不能只把输入类型写成 long long 就宣称安全。
`result=1%p` 让 b=0、p=1 也正确。
模意义下除法不能随便用整数除法替代。例如 (6/2)%5=3，但 (6%5)/2=0；模逆元是后续专题，且需要存在条件。

欧几里得算法需对数量级取对数的步骤，快速幂 O(log(b+1))，额外空间 O(1)。

## 完整 C++17 例题程序

独立源文件：[16-number-theory.cpp](../examples/16-number-theory.cpp)。输入输出约定见本章题目；程序针对题目保证的合法输入。

```cpp
#include <iostream>
using namespace std;

long long gcd_value(long long a, long long b) {
    while (b != 0) {
        long long remainder = a % b;
        a = b;
        b = remainder;
    }
    return a;
}

long long power_mod(long long base, long long exponent, long long modulus) {
    long long result = 1 % modulus;
    base %= modulus;
    while (exponent > 0) {
        if (exponent & 1LL) result = result * base % modulus;
        base = base * base % modulus;
        exponent >>= 1;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long a, b, p;
    if (!(cin >> a >> b >> p)) return 0;
    cout << gcd_value(a, b) << '\n';
    cout << power_mod(a, b, p) << '\n';
}
```

### 样例输入

```text
3 5 7
```

### 样例输出

```text
1
5
```

## 分层练习：先独立做，再展开答案

1. 手算 gcd(84,30) 的余数序列。
2. 计算 2^10 mod 1000，并将 10 拆成二进制位对应的幂。
3. 输入 `0 0 1` 时，两行各是什么？说明这里使用了什么约定。

<details>
<summary>参考答案与思路（先尝试再看）</summary>

1. `(84,30)→(30,24)→(24,6)→(6,0)`，答案 6。
2. 10=8+2，所以 2^10=2^8×2²=1024，余数 24。程序计算中可以每步先取模。
3. 0、0。约定 gcd(0,0)=0，指数为 0 的幂取 1，而 1 mod 1=0。明确题目约定后才谈程序行为。

</details>

## 过关标准

能证明 gcd 的余数等价；手算快速幂每轮状态；检查模乘中间结果是否溢出。

完成后在 [学习记录](../PROGRESS.md) 填写实际证据。看懂讲义、通过自带样例和独立掌握是三个不同阶段。

## 对照阅读

以下页面用于查阅术语与扩展。本文推导、示例与练习为独立编写，不是对 OI Wiki 原文的整页转载。

- [OI Wiki：最大公约数](https://oi-wiki.org/math/number-theory/gcd/)
- [OI Wiki：快速幂](https://oi-wiki.org/math/binary-exponentiation/)
- [OI Wiki：模运算](https://oi-wiki.org/math/number-theory/mod-arithmetic/)

[上一章](15-fenwick.md) · [返回目录](../README.md) · [下一章](17-kmp.md)
