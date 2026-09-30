---
title: 标准 KMP 模板：位置 + next 数组全输出（洛谷 P3375）
cards: [007]
source: 洛谷 P3375 · 【模板】KMP 字符串匹配
url: https://luogu.com.cn/problem/P3375
---

## 场景

比赛现场拿到字符串匹配题，你不想再现场推导一遍前缀函数——那就把洛谷 P3375 当肌肉记忆模板背下来。它要求输出所有匹配位置（1-indexed）和完整 next 数组，是 KMP 的标准形态：能默写这题，KMP 就毕业了。

## 信号

凡是"模式串自身有重复结构"的匹配题都该评估 KMP：模式如 "ababa"、"aaaa"，朴素法会在这类输入上反复回退。另一个信号是题目要求 O(n+m) 复杂度上限——这是 KMP 的复杂度签名，看到就该条件反射。

## 桥接

两个模块各自独立：build next（对模式串自己匹配自己）和 scan（文本上滑动）。求位置时在 `j == len(p)` 后令 `j = next[j-1]` 继续找——自重叠匹配（如 "AAAAA" 里找 "AA"）全靠这一步不漏解。1-indexed 输出只是 `i - len(p) + 2`，别让下标换算偷走你的 AC。

## 解答

```python
def kmp_template(s: str, p: str):
    """洛谷 P3375：返回 (所有匹配位置 1-indexed, next 数组 next[1..m])。"""
    nxt = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j > 0 and p[i] != p[j]:
            j = nxt[j - 1]
        if p[i] == p[j]:
            j += 1
            nxt[i] = j
    pos = []
    j = 0
    for i, ch in enumerate(s):
        while j > 0 and ch != p[j]:
            j = nxt[j - 1]
        if ch == p[j]:
            j += 1
        if j == len(p):
            pos.append(i - len(p) + 2)   # 题目要求 1-indexed
            j = nxt[j - 1]               # 继续找下一个（自重叠匹配）
    return pos, nxt

pos, nxt = kmp_template("ABABABC", "ABABC")
assert pos == [3] and nxt == [0, 0, 1, 2, 0]
pos, nxt = kmp_template("AAAAA", "AA")
assert pos == [1, 2, 3, 4] and nxt == [0, 1]
print("P3375 模板题两用例通过（匹配位置 + next 数组）")
```
