---
title: 宝物有数量上限的背包（洛谷 P1776 宝物筛选）
cards: [006]
source: 洛谷 P1776 · 宝物筛选
url: https://luogu.com.cn/problem/P1776
---

## 场景

阿里巴巴的宝藏洞有 n 种宝物，每种有 m_i 件，背包容积 W。选哪些、各拿几件能拿最大价值？朴素的"把每件都当独立物品做 01 背包"会超时——Σm_i 轻松上万，O(W·Σm) 直接爆炸。正解是把每种宝物的 m_i 件二进制拆分，这是多重背包的招牌技巧。

## 信号

"每种物品**有限数量**（既不是 1 也不是无限）"——多重背包。朴素拆法会 TLE 的信号也明显：n 很小（≤100）但每种数量很大（≤10000）。想起二进制拆分：1, 2, 4, ...,  remainder 这些包能拼出 0~m_i 的任何数量。

## 桥接

把 cnt 件拆成 1+2+4+...+2^k + 余数 共 O(log cnt) 个"打包物品"，每件内部不可分割（01 背包语义），外部随意组合。任何 0~cnt 的数量都能用这些包唯一凑出——二进制表示的本质。拆完直接套用 01 背包倒序模板，一个多余的字都不用写。

## 解答

```python
import random

def treasure(W: int, items: list) -> int:
    """多重背包：每种宝物 cnt 件。二进制拆分把 cnt 拆成 1+2+4+... 包，
    转成 01 背包，复杂度从 O(W·Σcnt) 降到 O(W·Σlog cnt)。"""
    packs = []
    for cnt, w, v in items:
        k = 1
        while cnt > 0:
            take = min(k, cnt)
            packs.append((take * w, take * v))
            cnt -= take
            k *= 2
    dp = [0] * (W + 1)
    for w, v in packs:
        for c in range(W, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]

def brute(W, items):  # 暴力枚举每种取几件，对拍验证
    best = 0
    def rec(i, rem, val):
        nonlocal best
        if i == len(items):
            best = max(best, val); return
        cnt, w, v = items[i]
        for k in range(min(cnt, rem // w) + 1):
            rec(i + 1, rem - k * w, val + k * v)
    rec(0, W, 0)
    return best

random.seed(1)
for _ in range(200):
    items = [(random.randint(1, 4), random.randint(1, 5), random.randint(1, 9)) for _ in range(4)]
    W = random.randint(5, 20)
    assert treasure(W, items) == brute(W, items)
print("二进制拆分与暴力枚举 200 组随机用例完全一致")
```
