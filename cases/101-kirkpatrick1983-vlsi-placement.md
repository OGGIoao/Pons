---
title: 芯片布图：百万个元件怎么摆（Kirkpatrick et al. 1983）
cards: [101]
source: Kirkpatrick, Gelatt & Vecchi, Science 220 (1983) · Optimization by Simulated Annealing
url: https://www.science.org/doi/10.1126/science.220.4598.671
---

## 场景

1983 年 IBM 的研究者面对的问题：一块芯片上几十万个门电路，摆在什么位置能使总连线长度最短？所有可能摆法远超宇宙原子数，穷举不存在；而且元件一旦密密麻麻卡死在一个局部拥挤的布局里，任何单点移动都只会更差——贪心从这儿永远出不去。这是模拟退火最著名的真实出身。

## 信号

三个特征同时出现就该想起它：① 解空间是**排列/组合**级别（n! 或 C(n,k)），没有解析最优解；② 目标函数**好算**（摆一下就能算出总线长），但搜索空间无法穷举；③ 你**容忍"够好"**而不是必须"最优"，且有明确的时间预算。

## 桥接

照搬冶金流程：高温时以接近随机的概率接受劣解（把元件从卡死布局里"震"出来），随温度衰减逐渐只接受好解，最后降温到纯贪心。Metropolis 准则 `P = exp(-Δ/T)` 一个公式就够，工程上再加"超时即停"的预算控制。

## 解答

```python
import math, random

def sa_place(blocks, wires, steps=20000, t0=50.0, t1=0.01):
    """blocks: 模块名列表；wires: [(a, b)] 连线对。
    模拟退火最小化总线长（Manhattan 距离），返回 (布局, 线长)。"""
    pos = {b: (random.random(), random.random()) for b in blocks}

    def wirelength(p):
        return sum(abs(p[a][0] - p[b][0]) + abs(p[a][1] - p[b][1])
                   for a, b in wires)

    cur = wirelength(pos)
    best, best_pos = cur, dict(pos)
    for k in range(steps):
        t = t0 * (t1 / t0) ** (k / steps)          # 几何降温
        a = random.choice(blocks)
        old = pos[a]
        pos[a] = (min(1, max(0, old[0] + random.gauss(0, t / 50))),
                  min(1, max(0, old[1] + random.gauss(0, t / 50))))
        nxt = wirelength(pos)
        if nxt <= cur or random.random() < math.exp((cur - nxt) / t):
            cur = nxt
            if cur < best:
                best, best_pos = cur, dict(pos)
        else:
            pos[a] = old                            # 拒绝：撤回这一步
    return best_pos, round(best, 2)

blocks = ["ALU", "REG", "MEM", "IO"]
wires = [("ALU", "REG"), ("ALU", "MEM"), ("REG", "MEM"), ("MEM", "IO")]
random.seed(42)
init = sum(abs(random.random() - random.random()) * 2 for _ in wires)
layout, wl = sa_place(blocks, wires)
print("退火后线长:", wl, "（随机布局约", round(init, 2), "）")
```
