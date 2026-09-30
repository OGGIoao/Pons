---
title: 大学排课表：约束互斥时怎么排出"冲突最少"的课表
cards: [101]
source: 运筹学经典问题 · University Timetabling（多所大学教务系统的真实实现）
---

## 场景

每学期开学前，教务要排出全校课表：几百门课、几十个教室、上百位教师，硬约束（教师不能分身、教室容量够）必须满足，软约束（教师偏好连排、课程尽量上午）尽量满足。纯手工排要两周，还必然有冲突。很多教务系统的排课引擎内部就是模拟退火（或其变种）。

## 信号

"约束太多且**互相打架**、没有标准答案、只求一个大家都过得去的方案"——这就是典型的组合优化泥潭。判断信号是：你能快速评价一个方案的好坏（数一下冲突数），但写不出一条规则直接构造出好方案。

## 桥接

先随便排出一个可行解（满足硬约束），然后反复做"邻域交换"：随机换两门课的时间/教室，冲突变少就接受，变多以 `exp(-Δ/T)` 的概率接受，温度慢慢降。跑 5 分钟拿到的课表，通常比人工迭代两周的冲突更少。

## 解答

```python
import math, random

def sa_schedule(exams, slots, conflicts, steps=20000, t0=30.0, t1=0.01):
    """exams: 考试科目；slots: 可用时段数；conflicts: 有学生同报的课程对。
    目标：把冲突对拆到不同时段，返回 (分配方案, 冲突数)。"""
    assign = {e: random.randrange(slots) for e in exams}

    def penalty(a):
        return sum(1 for x, y in conflicts if a[x] == a[y])

    cur = penalty(assign)
    best, best_a = cur, dict(assign)
    for k in range(steps):
        t = t0 * (t1 / t0) ** (k / steps)
        e = random.choice(exams)
        old = assign[e]
        assign[e] = random.randrange(slots)
        nxt = penalty(assign)
        if nxt <= cur or random.random() < math.exp((cur - nxt) / t):
            cur = nxt
            if cur < best:
                best, best_a = cur, dict(assign)
        else:
            assign[e] = old
    return best_a, best

exams = ["高数", "线代", "物理", "编程", "英语", "体育"]
conflicts = [("高数", "线代"), ("高数", "物理"), ("线代", "物理"),
             ("线代", "编程"), ("物理", "英语"), ("编程", "英语"),
             ("编程", "体育")]
random.seed(7)
plan, bad = sa_schedule(exams, slots=4, conflicts=conflicts)
assert bad == 0, f"仍有 {bad} 个冲突"
print("零冲突排课方案:", plan)
```
