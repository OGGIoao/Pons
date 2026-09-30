---
title: 缓存穿透攻击的挡箭牌：Redis 布隆过滤器
cards: [103]
source: Redis 官方模块 RedisBloom / 缓存穿透防护的经典工程实践
url: https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/
---

## 场景

恶意用户用不存在的用户 ID 刷你的接口：缓存查不到 → 每次都打穿到数据库，DB 被打挂。布隆过滤器是标准防线——把所有合法 ID 预先装进位数组，请求进来先问过滤器："这个 ID **一定不存在**吗？"答"不存在"直接拒绝，只有"可能存在"才放行查缓存/DB。

## 信号

查询型系统 + 恶意或随机的"查不存在数据"流量 + 存储放不下全量精确索引——布隆过滤器的出场条件。它的语义必须背熟：**说"不存在"一定对（零漏判），说"可能存在"有少量误伤**——拿它当"黑名单精确判定"就全用反了。

## 桥接

k 个哈希函数把元素映射成位数组里的 k 个坑，插入置 1、查询看是否全 1。内存约为精确哈希表的 1/10 ~ 1/100，代价是可控的误伤率——公式 (1-e^(-kn/m))^k 决定，调 m 和 k 即可换误伤率。代码不到 20 行，但先想语义再写：它只回答"一定不在"。

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

bf = BloomFilter(8192, 4)
for i in range(500):
    bf.add(f"user:{i}")
fp = sum(1 for i in range(500, 1500) if f"user:{i}" in bf) / 1000
assert all(f"user:{i}" in bf for i in range(500))   # 零漏判：说在就一定在过
assert fp < 0.05                                     # 误伤率可控
print(f"500 个 key / 8K 位 / 4 哈希：误伤率 {fp:.4f}（理论值约 0.002）")
```
