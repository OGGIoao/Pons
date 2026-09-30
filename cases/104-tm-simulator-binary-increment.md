---
title: 写一个通用图灵机模拟器：二进制加法机实践
cards: [104]
source: 图灵机编程经典练习 · 二进制加 1 机（各计算理论教材的标配示例）
---

## 场景

学完图灵机的五条指令（读、写、左移、右移、换状态），最好的验收方式是亲手写一台能跑的：给定规则表和纸带，模拟读写头一步步执行。二进制加 1 机是最经典的入门练习——走到最右端，再从右往左进位，规则和小学竖式一模一样，却覆盖了图灵机的全部要素。

## 信号

状态数量有限、动作由"当前状态 + 纸带符号"完全决定、有明确的停机状态——这三条就是图灵机的定义本身。看到"规则表 + 纸带 + 读写头"的表述，或在面试里被问"图灵机到底怎么运作"，就该想起这个 30 行的模拟器。

## 桥接

把规则表写成字典 `{(状态, 符号): (写, 移动, 下一状态)}`，主循环查表执行，纸带用列表 + 头指针模拟，两端自动补空白符 □。这一步走完，"存储程序计算机的理论基础"就不再是抽象名词——你写的正是 von Neumann 架构的最小原型。

## 解答

```python
def run_tm(tape: list, transitions: dict, start: str, max_steps: int = 10_000):
    """通用模拟器：{(状态, 读符号): (写符号, 移动 L/R/N, 下一状态)}。"""
    tape = list(tape)
    head, state, steps = 0, start, 0
    moves = {'L': -1, 'R': 1, 'N': 0}
    while state != 'halt' and steps < max_steps:
        w, m, state = transitions[(state, tape[head])]
        tape[head] = w
        head += moves[m]
        if head < 0:
            tape.insert(0, '□'); head = 0
        if head == len(tape):
            tape.append('□')
        steps += 1
    return tape, steps

# 二进制 +1 机：右移到尽头，再从右往左进位
trans = {
    ('start', '0'): ('0', 'R', 'start'), ('start', '1'): ('1', 'R', 'start'),
    ('start', '□'): ('□', 'L', 'carry'),
    ('carry', '0'): ('1', 'L', 'halt'), ('carry', '1'): ('0', 'L', 'carry'),
    ('carry', '□'): ('1', 'L', 'halt'),
}
tape, steps = run_tm(list('1011'), trans, 'start')
assert ''.join(tape).rstrip('□') == '1100'          # 11 + 1 = 12
print(f"二进制加 1：1011 → {''.join(tape).rstrip('□')}，{steps} 步停机")
```
