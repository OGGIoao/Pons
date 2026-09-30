---
title: 农产量约束互相矛盾了吗（洛谷 P1993 小K的农场）
cards: [003]
source: 洛谷 P1993 · 小K的农场
url: https://luogu.com.cn/problem/P1993
---

## 场景

小K的农场有 n 块田，调查队记录了 m 条断言："a 田产量至少比 b 田多 c 公斤"、"a 比 b 至多少 d"、"a 和 b 一样多"。有些记录来自互相矛盾的来源，你的任务是判断这组断言能否同时成立——这是差分约束的标准形态：一组不等式 + 一个"有没有解"的问题。

## 信号

关键词："x 比 y 多/少/不超过/不少于某个数"，变量之间只有差值关系、没有绝对值。一旦约束都能整理成 x_a - x_b ≤ c 或 ≥ c 的形式，就该想起：这是图上的最长路/最短路，环就是矛盾。

## 桥接

全部转成 x_a ≥ x_b + w 的边跑最长路，或转 ≤ 跑最短路，两种方向等价。判无解只看一件事：松弛迭代到第 n 轮还在更新 ⟺ 存在正环（或负环）⟺ 约束互相矛盾。加超级源点连所有变量，一次 SPFA 全搞定——这就是卡片里 Bellman-Ford 判负环的直接调用。

## 解答

```python
from collections import deque

def satisfiable(n: int, constraints: list) -> bool:
    """constraints: ('ge',a,b,c)→x_a-x_b≥c；('le',a,b,c)→x_a-x_b≤c；('eq',a,b)→x_a=x_b。
    全部转成 xa ≥ xb + w 的边，最长路判正环：有正环 = 约束互相矛盾。"""
    adj = [[] for _ in range(n)]
    for c in constraints:
        if c[0] == 'ge':   adj[c[2]].append((c[1], c[3]))
        elif c[0] == 'le': adj[c[1]].append((c[2], -c[3]))
        else:              adj[c[1]].append((c[2], 0)); adj[c[2]].append((c[1], 0))
    dist = [0] * n           # 超级源点：所有变量从 0 出发
    cnt = [0] * n
    inq = [True] * n
    q = deque(range(n))
    while q:
        u = q.popleft()
        inq[u] = False
        for v, w in adj[u]:
            if dist[u] + w > dist[v]:
                dist[v] = dist[u] + w
                if not inq[v]:
                    inq[v] = True
                    cnt[v] += 1
                    if cnt[v] >= n:
                        return False     # 正环 → 矛盾
                    q.append(v)
    return True

assert satisfiable(3, [('ge',0,1,1), ('ge',1,2,1), ('ge',2,0,1)]) is False  # x0>x1>x2>x0 死循环
assert satisfiable(3, [('ge',0,1,1), ('ge',1,2,1)]) is True
assert satisfiable(2, [('eq',0,1), ('ge',0,1,3)]) is False
print("环形矛盾被识破，合法约束全部通过")
```
