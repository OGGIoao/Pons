---
title: 用回溯生成所有合法括号串（LeetCode 22）
cards: [001]
source: LeetCode 22 · 括号生成
url: https://leetcode.cn/problems/generate-parentheses/
---

## 场景

你在写测试数据生成器：新功能是一个支持嵌套的规则配置器，QA 要求"生成所有合法嵌套结构做边界测试"。n=3 时有 5 种，n=4 时有 14 种——先知道这个总数，你才能判断测试集大小是否可接受，再决定用穷举还是抽样。

## 信号

需求里出现"**所有**合法嵌套/组合"且 n 很小（≤10）；或者评审时有人追问"这个结构的合法组合数到底有多少种"，你开始心算 1, 2, 5, 14……算到第四个数就该认出它了。

## 桥接

卡特兰数 Cₙ 直接给出总数（C₁₀ = 16796，穷举完全可行）。生成时用同一个约束做剪枝：任意前缀左括号 ≥ 右括号。先报总数、再回溯生成，这就是"结构同一性"的实战形态。

## 解答

```python
def generate_parentheses(n: int) -> list[str]:
    ans: list[str] = []

    def dfs(left: int, right: int, path: list[str]) -> None:
        if left == n and right == n:
            ans.append("".join(path))
            return
        if left < n:                 # 左括号随便放（只要没超 n）
            dfs(left + 1, right, path + ["("])
        if right < left:             # 右括号不能超过左括号——Catalan 约束
            dfs(left, right + 1, path + [")"])

    dfs(0, 0, [])
    return ans

assert sorted(generate_parentheses(3)) == sorted(
    ["((()))", "(()())", "(())()", "()(())", "()()()"])
assert generate_parentheses(1) == ["()"]
print("n=3 共", len(generate_parentheses(3)), "种 = Catalan(3)")
```
