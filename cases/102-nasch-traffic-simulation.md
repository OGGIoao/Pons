---
title: 堵车是怎么自发形成的：NaSch 交通流模型
cards: [102]
source: Nagel & Schreckenberg 1992 · A cellular automaton model for freeway traffic
---

## 场景

1992 年 Nagel 和 Schreckenberg 用一条环形车道和四条规则复现了真实交通的"幽灵堵车"：没有事故、没有红绿灯，仅凭"加速、跟车减速、随机慢化"三条局部规则，堵车波就会自发涌现。今天交通仿真、疏散模拟、网络拥塞研究里，元胞自动机仍是标准工具之一。

## 信号

系统由大量相同个体组成、个体只根据**邻居**做局部决策、却要求观察**全局**涌现行为（拥堵波、相变、临界点）——元胞自动机的信号。和生命游戏同构：局部规则简单，全局行为不可解析预测，只能模拟。

## 桥接

把道路离散成格子，每车有位置和速度，每步按"加速→减速(跟车间距)→以概率 p 随机慢化→前进"更新——四条规则，和生命游戏的四条生存法则一一对应。随机慢化一项是灵魂：去掉它车流永不堵车；有了它，密度一过临界值堵车波自发出现。这就是"复杂从简单涌现"最直观的实验场。

## 解答

```python
import random

def nasch(length: int, positions: list, steps: int, vmax: int = 5, p: float = 0.3, seed: int = 0) -> list:
    """Nagel–Schreckenberg 交通流模型：加速→减速(跟车)→随机慢化→移动。
    返回 step 步后的 [(位置, 速度)]，环形道路。"""
    rng = random.Random(seed)
    cars = sorted((x, rng.randint(0, vmax)) for x in positions)
    for _ in range(steps):
        nxt = []
        for i, (x, v) in enumerate(cars):
            gap = (cars[(i + 1) % len(cars)][0] - x - 1) % length
            v = min(v + 1, vmax)             # 加速：都想开快
            v = min(v, gap)                  # 减速：不许追尾
            if rng.random() < p:
                v = max(v - 1, 0)            # 随机慢化：堵车之源
            nxt.append(((x + v) % length, v))
        cars = sorted(nxt)
    return cars

final = nasch(50, [0, 10, 20, 30, 40], 100)
assert len(final) == 5
assert len({x for x, _ in final}) == 5, "发生追尾——模型写错了"
print("100 步演化：5 辆车无一追尾，交通流守恒")
```
