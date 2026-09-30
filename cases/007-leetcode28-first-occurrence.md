---
title: 手写 strstr：模式匹配的第一课（LeetCode 28）
cards: [007]
source: LeetCode 28 · Find the Index of the First Occurrence in a String
url: https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/
---

## 场景

你的日志告警系统要在大段日志流里找第一个异常模式出现的位置。调库一行 `str.find` 就完事——但如果面试官追问"它为什么快"，或者你被要求处理流式数据、需要边读边匹配，KMP 就是必答题。LC28 是它最朴素的出场方式。

## 信号

"长文本里找模式"、"要求 O(n+m)"、"不能用内置查找"——KMP 三信号。朴素双循环是 O(nm)，一旦文本和模式都带大量重复结构（如 "aaaa…a" 里找 "aaa"），朴素法会反复回退文本指针，复杂度退化的场景就是 KMP 的用武之地。

## 桥接

核心思想一句话：文本指针 i **永不回退**。失配时根据"已匹配部分的最长公共前后缀"（前缀函数 next 数组）移动模式指针 j，跳过的部分已被数学保证不可能匹配。预处理模式串一次 O(m)，匹配 O(n)，全程零回退——解答就是卡片参考实现去掉注释后的最小骨架。

## 解答

```python
def str_str(haystack: str, needle: str) -> int:
    if not needle: return 0
    nxt = [0] * len(needle)          # 前缀函数：失配时模式指针回退到哪里
    j = 0
    for i in range(1, len(needle)):
        while j > 0 and needle[i] != needle[j]:
            j = nxt[j - 1]
        if needle[i] == needle[j]:
            j += 1
            nxt[i] = j
    j = 0                            # 文本指针永不回退，只有模式指针跳
    for i, ch in enumerate(haystack):
        while j > 0 and ch != needle[j]:
            j = nxt[j - 1]
        if ch == needle[j]:
            j += 1
        if j == len(needle):
            return i - len(needle) + 1
    return -1

assert str_str("sadbutsad", "sad") == 0
assert str_str("leetcode", "leeto") == -1
assert str_str("ababcababa", "ababa") == 5
print("KMP 三用例通过（含自重叠模式）")
```
