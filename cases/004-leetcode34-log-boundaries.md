---
title: 日志系统查"某事件第一次/最后一次出现的时间"（LeetCode 34）
cards: [004]
source: LeetCode 34 · 在排序数组中查找元素的第一个和最后一个位置
url: https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/
---

## 场景

你的日志服务按时间戳有序存储了 10⁸ 条记录。运营问："用户 8848 的支付失败最早出现在哪天？最近一次是哪天？"你写查询时发现，`bisect_left(ts, user_id)` 拿到左边界、`bisect_right` 拿到右边界，一次查询 O(log n)，比扫全表快六个数量级。

## 信号

关键词组合："**有序**" + "找**第一个/最后一个/不小于/不大于**"。注意陷阱：不是"找值"——找值命中即停，找边界必须处理"等于但要继续收缩"的那一侧。写二分模板时 if 分支里 `lo = mid + 1` 还是 `hi = mid`，错一个符号就死循环或漏解。

## 桥接

背一个 lower_bound 模板（求第一个 ≥ target 的位置），右边界用 `bisect_right` 对称得到。所有"有序 + 边界"问题都是它的换皮：Python 标准库 `bisect`、C++ `lower_bound`、Java `Collections.binarySearch`，语义完全一致。

## 解答

```python
def search_range(nums: list[int], target: int) -> list[int]:
    def lower_bound(t: int) -> int:      # 第一个 >= t 的下标（左闭右开）
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < t:
                lo = mid + 1             # mid 在答案左边，砍掉
            else:
                hi = mid                 # mid 可能就是答案，保住
        return lo

    first = lower_bound(target)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    return [first, lower_bound(target + 1) - 1]  # 右边界 = 第一个 > target - 1

assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]
assert search_range([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
assert search_range([], 0) == [-1, -1]
print("边界查找三用例通过")
```
