---
title: 减约数游戏里的奇偶陷阱（LeetCode 1025 Divisor Game）
cards: [002]
source: LeetCode 1025 · Divisor Game
url: https://leetcode.cn/problems/divisor-game/
---

## 场景

爱丽丝和鲍勃玩游戏：给定数字 n，每回合必须选一个真约数 x 把 n 减去它，谁先把数减到 1 谁赢。这题的陷阱在于：绝大多数人开始写记忆化搜索，而真正上场打比赛的人需要一个 O(1) 结论——这正是"必胜/必败逆推"练到家的样子。

## 信号

博弈题里先算小的：n=1 必败（没得选）、n=2 必胜（减 1）、n=3 必败、n=4 必胜……列出前几项找周期。另一个信号是"操作把数严格变小"——这保证了逆推的拓扑序天然存在，和 Nim 的模周期是同一类手法。

## 桥接

答案藏在奇偶里：偶数必胜。策略是"先手永远减 1，把奇数交给对手"——奇数的约数必为奇数，奇减奇得偶，对手只能把偶数还回来，如此往复，对手最终面对 1。逆推证明与构造策略一步到位，这是博弈论卡片的招牌动作。

## 解答

```python
def divisor_game(n: int) -> bool:
    # 偶数必胜：先手减 1 把奇数交给对手；奇数的因子必为奇数，
    # 奇-奇=偶——对手只能把偶数还回来，最终对手拿到 1。
    return n % 2 == 0

def brute(n: int) -> bool:  # 记忆化穷举对拍
    from functools import lru_cache
    @lru_cache(None)
    def win(x: int) -> bool:
        return any(not win(x - d) for d in range(1, x) if x % d == 0)
    return win(n)

assert all(divisor_game(i) == brute(i) for i in range(1, 21))
print("n=1..20 与暴力对拍全部一致：偶数必胜")
```
