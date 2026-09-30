---
title: 凑零钱有多少种凑法（LeetCode 518 零钱兑换 II）
cards: [006]
source: LeetCode 518 · Coin Change II
url: https://leetcode.com/problems/coin-change-2/
---

## 场景

收银系统升级：给定面额和总额，问有多少种凑法。注意是"组合"——1+2 和 2+1 算同一种。这题栽人最多：写出来能跑，答案却总是偏大——把组合数成了排列。它是完全背包的计数版，循环顺序就是题眼。

## 信号

"凑出目标值"、"物品无限"、"问**多少种**"——计数版完全背包。判定组合还是排列只看一层：硬币在循环外层 → 每种硬币的"用不用、用几次"先定序 → 组合；金额在外层 → 每种面额的决策被拆开交错 → 排列。同一个 dp 数组，语义由循环嵌套决定。

## 桥接

dp[s] += dp[s - coin]，硬币在外层、正序金额在内层。加法语义天然：凑出 s 的方法 = 所有"先用了某 coin、再凑出 s-coin"的方法之和。01 背包的 or、最值背包的 max、计数背包的 +——值域操作换了，骨架还是那个二维表压成一维。

## 解答

```python
def change(amount: int, coins: list) -> int:
    """凑出 amount 的组合数：硬币在外层循环 → 每种硬币"用不用"先定序，是组合不是排列。"""
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for s in range(coin, amount + 1):
            dp[s] += dp[s - coin]
    return dp[amount]

assert change(5, [1, 2, 5]) == 4   # 5 / 2+2+1 / 2+1+1+1 / 1×5
print("凑 5 分共有 4 种组合")
```
