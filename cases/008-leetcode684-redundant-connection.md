---
title: 树里多了一条边，揪出它（LeetCode 684 冗余连接）
cards: [008]
source: LeetCode 684 · Redundant Connection
url: https://leetcode.cn/problems/redundant-connection/
---

## 场景

有一棵 n 个节点的树（无环连通图），有人多画了一条边，图里出现了一个环。要求找出这条多余的边。例如 `[[1,2],[1,3],[2,3]]` 里 `[2,3]` 是冗余的——它让 2 和 3 所在的已连通部分成环。输入按加边顺序给出，答案要取**最后出现**的那条冗余边。

## 信号

边逐条加入、每加一条都要回答"这两点之前是否已经连通"——这正是并查集查询的标准信号。凡是无向图判环、连通性判定、"这条边是否真的连接了两个不同分量"的问题，都不需要真的建图跑 DFS。

## 桥接

把「加一条边」直接翻译成 union，把「是否成环」翻译成 union 的返回值：边的两端 find 出来是同一个代表，说明这条边连接的是已经同门的两个人——加上它必成环。顺着输入顺序扫描，union 返回 False 的边就是冗余边。逐条处理天然满足"取最后一条"的要求。

## 解答

```python
def find_redundant_connection(edges):
    """逐条 union，第一次合并失败（两端已连通）的边即冗余边。"""
    parent = {}

    def find(x):
        if x not in parent:
            parent[x] = x
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]               # 已连通 → 这条边是环的元凶
        parent[ra] = rb
    return []

assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
```
