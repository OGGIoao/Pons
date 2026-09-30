---
title: 奶牛排队列：间距的上界与下界（POJ 3169 Layout）
cards: [003]
source: POJ 3169 · Layout
url: http://poj.org/problem?id=3169
---

## 场景

n 头奶牛按编号排成一列吃草，1 号固定在 0 号位。饲养员记录了两类约束：某些相邻奶牛"最多相隔多少"，某些关系好的奶牛"至少相隔多少"。问 1 号和 n 号最远能隔多远——约束有矛盾就输出 -1，没有上界就输出 -2。这是差分约束从"判矛盾"升级到"求最优值"的标准题。

## 信号

变量是位置，约束全是"间距 ≤ 上界 / ≥ 下界"的不等式组，求某个差值的最值——这就是"差分约束 + 最短路"的完整信号。注意它有两种不稳定结局（矛盾 / 无界），对应负环和不可达，判题时别只考虑"求出一个数"。

## 桥接

上界 d[b] - d[a] ≤ w 是最短路边 a→b(w)；下界 d[b] - d[a] ≥ c 翻成 d[a] ≤ d[b] - c，即边 b→a(-c)。从 1 号跑 Bellman-Ford：第 n 轮仍能松弛 ⟺ 负环 ⟺ 矛盾输出 -1；n 号不可达 ⟺ 无上界输出 -2；否则 dist[n] 就是答案。三个出口，一个模板，全是卡片里现成的零件。

## 解答

```python
def max_layout(n: int, at_most: list, at_least: list):
    """POJ 3169：1 号奶牛固定在 0，2..n 按序号排在它右边（位置可以重合）。
    at_most=[(a,b,d)]：d[b]-d[a] ≤ d；at_least=[(a,b,d)]：d[b]-d[a] ≥ d。
    返回 1→n 的最大合法距离；矛盾 -1；无上界 -2。"""
    INF = float('inf')
    adj = [[] for _ in range(n + 1)]
    for a, b, d in at_most:
        adj[a].append((b, d))          # 上界：d[b] ≤ d[a] + d（最短路边）
    for a, b, d in at_least:
        adj[b].append((a, -d))         # 下界：d[a] ≤ d[b] - d（反向边）
    dist = [INF] * (n + 1)
    dist[1] = 0
    for k in range(n):
        updated = False
        for u in range(1, n + 1):
            if dist[u] == INF: continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
                    if k == n - 1: return -1    # 第 n 轮仍松弛 = 负环 = 矛盾
        if not updated: break
    return -2 if dist[n] == INF else dist[n]

assert max_layout(4, [(1,2,2),(2,3,3),(3,4,2)], [(1,4,6)]) == 7   # 上界 7、下界 6 → 取 7
assert max_layout(4, [(1,2,2),(2,3,3),(3,4,2)], [(1,4,10)]) == -1 # 下界超过上界 → 矛盾
assert max_layout(4, [], [(1,4,6)]) == -2                         # 没有上界 → 无穷大
print("POJ 3169 三种结局（7 / -1 / -2）全部正确")
```
