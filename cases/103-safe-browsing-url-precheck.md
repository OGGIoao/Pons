---
title: 浏览器怎么快速预检恶意网址（布隆过滤器的经典应用）
cards: [103]
source: Google Safe Browsing 早期版本公开技术记录 · Bloom filter 预筛恶意网址的经典案例
---

## 场景

浏览器每打开一个网页都要查"这个网址在不在恶意名单里"。名单有几千万条，每次联网查太慢，把全量哈希表塞进浏览器又太大——早期 Chrome 的 Safe Browsing 用布隆过滤器做本地预筛：名单置进位数组，本地判断"一定干净"直接放行，只有"可能恶意"才联网确认。误伤几条正常网址，换来毫秒级响应和 1/60 的内存。

## 信号

"海量集合 + 频繁查询 + 内存放不下精确结构 + 容忍极小误伤率"——布隆过滤器的四要素。和缓存穿透是同一个模式的两个方向：那边挡"不存在"，这边挡"可能存在"——都是拿确定性换空间。

## 桥接

哈希表存的是 URL 本身，布隆存的是"指纹位"：m 位的数组 + k 个哈希，插入即置位。误伤率随装入元素数上升，公式 (1-e^(-kn/m))^k 可预先算好容量规划。删除是布隆的禁区（置 1 会误伤共享位的元素）——需要删除就上 Counting Bloom，那是后话。

## 解答

```python
import hashlib

class BloomFilter:
    """位数组 + k 个哈希函数：插入置位，查询看 k 位是否全为 1。"""
    def __init__(self, size: int, hashes: int):
        self.bits, self.size, self.hashes = 0, size, hashes
    def _seeds(self, s: str):
        for i in range(self.hashes):
            yield int(hashlib.md5(f"{i}:{s}".encode()).hexdigest(), 16) % self.size
    def add(self, s: str) -> None:
        for b in self._seeds(s):
            self.bits |= 1 << b
    def __contains__(self, s: str) -> bool:
        return all(self.bits >> b & 1 for b in self._seeds(s))

blacklist = [f"evil-{i}.com" for i in range(1000)]
bf = BloomFilter(16384, 5)
for u in blacklist:
    bf.add(u)
assert "evil-0.com" in bf and "evil-999.com" in bf   # 黑名单零漏判
fp = sum(1 for i in range(1000) if f"safe-{i}.com" in bf) / 1000
assert fp < 0.02
print(f"16K 位拦 1000 条恶意网址：误伤率 {fp:.4f}，内存约为哈希表的 1/60")
```
