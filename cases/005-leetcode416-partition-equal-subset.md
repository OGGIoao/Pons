---
title: 数组能不能分成和相等的两组（LeetCode 416 分割等和子集）
cards: [005]
source: LeetCode 416 · Partition Equal Subset Sum
url: https://leetcode.cn/problems/partition-equal-subset-sum/
---

## 场景

队友扔给你一道"中等"题：给定数组，能否分成两个和相等的子集？表面看是集合划分，没有任何背包字样；但"选一部分数使它们的和恰为目标值"——这就是背包容量等于目标和、物品重量等于数值、价值等于数值的 01 背包。卡壳的人卡在没认出它。

## 信号

题目里完全没有"背包"二字，但出现："选**一部分**元素"、"凑出**恰好**某个和"、"能否"（可行性而非最值）——这就是可行性版 01 背包，dp 值从"最大价值"退化成"布尔可达"。先判总和奇偶：奇数直接 False，连表都不用建。

## 桥接

dp[s] = 能否凑出和 s。逐个放入数字 x：可行性沿"倒序 s 从 target 到 x"传递，dp[s] |= dp[s-x]。和 P1048 同一张表，只是 max 换成 or——背包的"形"没变，"值域"换了。会这一层，子集和、目标和、最小差值划分全是一家人。

## 解答

```python
def can_partition(nums: list) -> bool:
    total = sum(nums)
    if total % 2: return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1):   # 每个数只能用一次 → 倒序
            dp[s] |= dp[s - x]
    return dp[target]

assert can_partition([1, 5, 11, 5]) is True
assert can_partition([1, 2, 3, 5]) is False
print("能/不能平分两组用例均正确")
```
