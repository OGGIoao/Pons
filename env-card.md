# 环境需求卡 · Env Card

> 脑桥的卡片分为不同依赖层级。查这张卡，看你选的卡需要什么环境。

---

## 按卡片查

| 卡片 | 需要安装 | 一句话 |
|------|---------|--------|
| 001 卡特兰数 | **无**（纯 Python 标准库） | 打开就能跑 |
| 002 博弈论 | **无**（纯 Python 标准库） | 打开就能跑 |
| 003 差分约束 | **无**（纯 Python 标准库） | 打开就能跑 |
| 101 数学可视化翻译 | `numpy`, `matplotlib`, `scipy` | pip 一次，全系列用 |
| 102 机器学习基础 | `scikit-learn`, `numpy`, `matplotlib` | 在 101 基础上加一个 |
| 103 深度学习入门 | `torch`, `torchvision` | 需要 CUDA（可选） |

---

## 按层级装

### 🟢 零依赖（所有纯算法思维卡）

```bash
# 什么都不用装。打开 Python，直接写。
```

### 🟡 最小可视化环境

```bash
pip install numpy matplotlib scipy
```

适用：L1 翻译器的所有内容 + 数学可视化相关卡的示例代码

### 🔵 机器学习环境

```bash
pip install numpy matplotlib scipy scikit-learn
```

### 🔴 深度学习环境

```bash
# CPU 版
pip install torch torchvision

# GPU 版（需 NVIDIA 显卡 + CUDA）
# 去 https://pytorch.org 选你的配置
```

---

## 一张卡一张环境？太麻烦？

不用。这条命令安装 90% 卡片的依赖：

```bash
pip install numpy matplotlib scipy scikit-learn
```

只有深度学习那张需要额外装 PyTorch。
