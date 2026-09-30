---
title: 校验撤销/重做日志的合法性（LeetCode 946）
cards: [001]
source: LeetCode 946 · 验证栈序列
url: https://leetcode.cn/problems/validate-stack-sequences/
---

## 场景

你在实现编辑器的"撤销/重做"功能，并需要校验一份录制下来的操作回放日志：给定"入栈顺序"（用户执行操作的顺序）和"出栈顺序"（回放时撤销的顺序），判断这份日志是不是一次合法的操作历史。线上出现过后回放死循环的 bug，根因就是日志不合法。

## 信号

问题变成"**两个序列，问能不能**"——不是问有多少种，而是问给定的一对序列是否满足某种先后约束。凡是可以抽象成"进/出两个动作的交错"的系统（括号、列车编组、函数调用与返回），都进入卡特兰数的领地。

## 桥接

用贪心模拟：按出栈序列依次检查，栈顶不匹配就持续入栈直到匹配，最终栈空即合法。它的判定对象正是全体出栈序列——其数量恰好是卡特兰数，所以这个模拟器"会接受多少种日志"是可以预先算出来的。

## 解答

```python
def validate_stack_sequences(pushed: list[int], popped: list[int]) -> bool:
    stack: list[int] = []
    j = 0  # popped 里下一个要弹出的位置
    for x in pushed:
        stack.append(x)
        # 栈顶恰好是"下一个该弹的"就持续弹——弹不出顺序就是非法
        while stack and j < len(popped) and stack[-1] == popped[j]:
            stack.pop()
            j += 1
    return not stack  # 全部弹完才算合法

assert validate_stack_sequences([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]) is True
assert validate_stack_sequences([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]) is False
print("两组用例均通过")
```
