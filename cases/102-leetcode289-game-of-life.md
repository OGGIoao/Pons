---
title: 原地演化的生命游戏（LeetCode 289）
cards: [102]
source: LeetCode 289 · Game of Life
url: https://leetcode.cn/problems/game-of-life/
---

## 场景

你在写一个网格模拟器：每个格子的生死由邻居数决定，要求一次刷新全体同步更新，且不能用 O(mn) 额外空间。这就是康威生命游戏的工程版——元胞自动机思想的最小实战：局部规则、全局涌现、状态同步。

## 信号

"网格 / 棋盘 + 每个单元的状态由邻居决定 + 全体**同时**更新"——元胞自动机三件套。同步更新是陷阱所在：先写死再改会串味（用了别人的新状态），解法是把"下一状态"编码进格子本身，一次性收割。

## 桥接

用二进制第二位存下一状态：`01→11`（活且续活）、`00→10`（死而复生），最后统一右移。判断邻居时用 `& 1` 取当前位，新旧状态在一格里和平共处——状态编码是位运算的经典应用，也是生命游戏"简单规则产生复杂行为"思想在代码层的倒影。

## 解答

```python
def game_of_life(board: list) -> None:
    """原地 O(1) 额外空间：用二进制第二位记录下一状态，最后整体右移。"""
    m, n = len(board), len(board[0])
    for r in range(m):
        for c in range(n):
            live = sum(board[i][j] & 1 for i in range(max(0, r - 1), min(m, r + 2))
                       for j in range(max(0, c - 1), min(n, c + 2)) if (i, j) != (r, c))
            if board[r][c] == 1 and live in (2, 3):
                board[r][c] = 3            # 01 → 11：这一位仍表示"现在活"
            elif board[r][c] == 0 and live == 3:
                board[r][c] = 2            # 00 → 10
    for r in range(m):
        for c in range(n):
            board[r][c] >>= 1

b = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]   # 经典"闪烁器"
game_of_life(b)
assert b == [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
print("闪烁器演化一步正确")
```
