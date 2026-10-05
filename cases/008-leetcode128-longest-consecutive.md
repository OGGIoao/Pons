---
title: 未排序数组里的最长连续序列（LeetCode 128）
cards: [008]
source: LeetCode 128 · Longest Consecutive Sequence
url: https://leetcode.cn/problems/longest-consecutive-sequence/
---

## 场景

给一个没排序的数组 `[100, 4, 200, 1, 3, 2]`，要求 O(n) 时间找出最长连续序列的长度（这里是 4：`1,2,3,4`）。排序是 O(n log n)，直接出局；想在 O(n) 内解决，必须把"连续"这个关系本身当成连边操作来做。

## 信号

三个信号同时出现就该想起并查集：① 元素之间存在天然的"相邻/同类"关系（x 和 x+1 是同类）；② 要把同类元素聚成簇再统计簇的大小；③ 要求线性或近线性复杂度。凡是"关系可传递 + 要数最大一群"的题，都是同一个骨架。

## 桥接

把每个数当成一个节点，只要 `x+1` 也在数组里，就把 `x` 和 `x+1` 合并——答案就是合并完成后最大的集合大小。并查集顺手维护每个集合的元素个数，合并时累加即可。每个元素至多被合并两次（和 x-1、和 x+1），整体严格 O(n·α(n))。

## 解答

```python
def longest_consecutive(nums):
    """O(n) 求最长连续序列：相邻的数并入同一集合，维护集合大小。"""
    parent = {}
    size = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for x in nums:
        if x in parent:
            continue                    # 重复元素不处理
        parent[x] = x
        size[x] = 1
        for y in (x - 1, x + 1):        # 只和相邻的数合并
            if y in parent:
                rx, ry = find(x), find(y)
                if rx != ry:
                    parent[rx] = ry
                    size[ry] += size[rx]
    return max(size.values(), default=0)

assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 1]) == 9
assert longest_consecutive([]) == 0
```
