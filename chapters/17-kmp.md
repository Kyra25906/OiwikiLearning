# 第 17 章 · 字符串与 KMP：失配之后保留已经匹配的信息

[返回目录](../README.md) · [上一章](16-number-theory.md) · [下一章](18-integration.md)

**先修知识：** 第 01、02 章；熟悉 0-based 数组和循环不变量。

**本章完成后：** 推导前缀函数，理解失配跳转，并找出所有允许重叠的匹配位置。

**建议学习方式：** 分两次完成。第一次读推导并手算，第二次盖住代码独立实现、做题和复盘。复杂章节可增加课次，不必一次读完。

## 1. 字符串匹配到底输出什么

输入文本 text 与模式 pattern，均为不含空白的非空小写字母串，长度各不超过 200000。
找出 pattern 在 text 中出现的所有起始位置，按从小到大输出，位置从 0 开始；允许重叠。不存在则输出 -1。
例如 text=`ababa`、pattern=`aba`，答案是 0 和 2。
本例按 char 处理 ASCII 字母，不能直接把 UTF-8 中文的一个字节当成一个汉字位置。

## 2. 朴素匹配浪费了什么

对每个起点从 pattern[0] 开始匹配，失配后整体右移一格再从头来，最坏 O(nm)。
已经匹配的一段字符往往包含可复用的前后缀。例如已经匹配 `ababa`，它的后缀 `aba` 同时也是模式开头的 `aba`。
即使后面失配，也不必忘记这三字符的信息。

## 3. 先只研究模式串自己：前缀函数

pi[i] 定义为 pattern[0..i] 的“最长相等真前缀与后缀”的长度。
真前缀不包含整段本身，否则答案总是 i+1，没有帮助。
例如模式 `ababa`：

| i | 前 i+1 个字符 | 最长相等真前后缀 | pi[i] |
|---:|---|---|---:|
| 0 | a | 空 | 0 |
| 1 | ab | 空 | 0 |
| 2 | aba | a | 1 |
| 3 | abab | ab | 2 |
| 4 | ababa | aba | 3 |

计算 pi[i] 时，先尝试延长上一段最长边界 j=pi[i-1]。
若 pattern[i]==pattern[j]，长度可以增加 1；否则当前边界无法延长，退到它自身的最长边界 `j=pi[j-1]`，再尝试。

## 4. 为什么是 pi[j-1]，而不是 j-1

已匹配的长度 j 对应 pattern[0..j-1]。若要保留它结尾的一段作为新的模式开头，这一段必须同时是它的前缀和后缀。
最长可保留长度正是 pi[j-1]，更短候选继续沿同样的链寻找。
单纯 j-- 并不能保证保留部分与模式前缀相同；回到 0 虽然可用于朴素重试，却会失去复用信息的效率。

## 5. 用同一套失配跳转扫描文本

j 表示“当前文本后缀已经匹配模式的前 j 个字符”。读 text[i] 时，失配就沿 pi 回退；匹配则 ++j。
当 j 等于模式长度 m，找到一次匹配，起点为 i-m+1。
记录后令 j=pi[m-1]，保留可以重叠的后缀。对 `ababa` 匹配 `aba`，第一次结束在 i=2，回退到 j=1，保留末尾 a；随后还能得到起点 2。

## 6. 正确性与线性复杂度

每次回退都转向仍可能与当前文本后缀相等的模式前缀，且按长度从大到小尝试，不会跳过一个可行的更长候选。
文本下标只前进，j 每读一个字符至多增加 1，所有回退减少量受累计增加量限制，因此扫描总工作 O(n)。构造 pi 同理 O(m)。
总时间 O(n+m)。pi 占 O(m)，示例保存输入和答案后总空间 O(n+m)。
条件判断必须先检查 j>0，再访问 pi[j-1]。匹配完成后及时回退，避免下一轮访问 pattern[m]。

## 完整 C++17 例题程序

独立源文件：[17-kmp.cpp](../examples/17-kmp.cpp)。输入输出约定见本章题目；程序针对题目保证的合法输入。

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string text, pattern;
    if (!(cin >> text >> pattern)) return 0;
    int n = static_cast<int>(text.size());
    int m = static_cast<int>(pattern.size());
    vector<int> pi(m, 0);
    for (int i = 1; i < m; ++i) {
        int j = pi[i - 1];
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];
        if (pattern[i] == pattern[j]) ++j;
        pi[i] = j;
    }
    vector<int> positions;
    int j = 0;
    for (int i = 0; i < n; ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j - 1];
        if (text[i] == pattern[j]) ++j;
        if (j == m) {
            positions.push_back(i - m + 1);
            j = pi[j - 1];  // 保留重叠部分
        }
    }
    if (positions.empty()) cout << -1;
    else {
        for (int i = 0; i < static_cast<int>(positions.size()); ++i) {
            if (i) cout << ' ';
            cout << positions[i];
        }
    }
    cout << '\n';
}
```

### 样例输入

```text
ababa
aba
```

### 样例输出

```text
0 2
```

## 分层练习：先独立做，再展开答案

1. 手算 `aaaa` 的 pi 数组。
2. text=`aaaaa`、pattern=`aaa` 的所有匹配起点是什么？
3. 如果找到匹配后把 j 直接清零，哪类答案可能漏掉？给一个反例。

<details>
<summary>参考答案与思路（先尝试再看）</summary>

1. `[0,1,2,3]`，每个前缀都能保留去掉一个字符后的相等前后缀。
2. 0、1、2。长度为 3 的模式可在长度为 5 的文本中重叠出现三次。
3. 会漏重叠匹配。例如 ababa 中的 aba，第一次匹配后若清零，就不能利用已读到的最后一个 a，可能漏掉起点 2。

</details>

## 过关标准

能手算 pi；能解释 j 的含义、pi[j-1] 的来源及重叠匹配回退。

完成后在 [学习记录](../PROGRESS.md) 填写实际证据。看懂讲义、通过自带样例和独立掌握是三个不同阶段。

## 对照阅读

以下页面用于查阅术语与扩展。本文推导、示例与练习为独立编写，不是对 OI Wiki 原文的整页转载。

- [OI Wiki：字符串基础](https://oi-wiki.org/string/basic/)
- [OI Wiki：前缀函数与 KMP 算法](https://oi-wiki.org/string/kmp/)

[上一章](16-number-theory.md) · [返回目录](../README.md) · [下一章](18-integration.md)
