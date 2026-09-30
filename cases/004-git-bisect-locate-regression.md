---
title: 上千个 commit 里定位引入性能回退的那一个（git bisect）
cards: [004]
source: git 官方文档 · git-bisect
url: https://git-scm.com/docs/git-bisect
---

## 场景

用户反馈"上个季度还好的导出功能，这周慢得没法用"。release 分支上隔着上千个 commit，你不可能逐个 checkout 手工验证。真实解法：`git bisect start` 标记当前版本为 bad、上个季度 tag 为 good，然后 `git bisect run ./benchmark.sh`——Git 自动二分 checkout，十几步就锁定肇事 commit。

## 信号

三个条件同时成立就该想起它：① 结果可判定（有个脚本/命令能输出 good 或 bad）；② 版本按时间或提交序排列；③ 你正在线性遍历版本。满足"单调谓词"的一切场景——查故障、查回退、查引入某行代码的版本——都是同一个模式。

## 桥接

把"问题存不存在"写成一个退出码为 0/1 的判定脚本，交给 bisect 自动驱动。二分的本质是在单调谓词上找边界：good 全在左、bad 全在右，每次测试砍掉一半搜索空间，log₂(1000) ≈ 10 次测试足矣。

## 解答

```python
import subprocess

def auto_bisect(bad_now: str, good_tag: str, test_cmd: list[str]) -> str:
    """全自动二分定位：git 自己检出中间版本，跑 test_cmd 判定好坏。
    返回引入回退的 commit 哈希。"""
    def judge() -> str:
        ok = subprocess.run(test_cmd, capture_output=True).returncode == 0
        return "good" if ok else "bad"

    subprocess.run(["git", "bisect", "start", bad_now, good_tag], check=True)
    try:
        while True:
            out = subprocess.run(["git", "bisect", judge()],
                                 capture_output=True, text=True).stdout
            first_bad = [l for l in out.splitlines() if "first bad commit" in l]
            if first_bad:                      # git 已锁定肇事 commit
                return out.split()[-1]
    finally:
        subprocess.run(["git", "bisect", "reset"], check=True)

# 真实仓库里这样用（测试命令随意换）：
# culprit = auto_bisect("HEAD", "v2.4.0", ["python3", "perf_test.py"])
# print("肇事 commit:", culprit)
```
