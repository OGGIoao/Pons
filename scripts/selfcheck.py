#!/usr/bin/env python3
"""Pons 自检脚本：提取每张卡的「参考实现 + 自测用例」并运行，验证全部通过。

用途：
  - 一键确认所有卡片的参考实现与自测断言彼此一致（防回归）。
  - 修改卡片后跑一次，立即发现「参考代码」或「文档数字」是否写错。

用法（零依赖，纯标准库）：
  python3 scripts/selfcheck.py

原理：
  - 从每张卡的阶段四提取「🧪 自测用例」的 python 代码块，
    以及「### 参考实现 → ### 这个模式还出现在……」之间的 python 代码块。
  - 先执行参考实现（定义函数），再执行自测断言。
  - 以 __name__="selfcheck" 运行，让 demo 函数（如 glider_demo）的
    if __name__ == "__main__" 守卫不触发，避免真正的动画/死循环。
"""
import contextlib
import io
import re
import sys
from pathlib import Path

PATTERNS = Path(__file__).resolve().parent.parent / "patterns"

# 卡片清单自动发现：glob patterns/*.md（排除 _template 与 catalog），
# 与 pons-web/scripts/build-cards.mjs 的发现逻辑保持一致——新卡零登记。
CARDS = sorted(
    p.stem
    for p in PATTERNS.glob("*.md")
    if not p.stem.startswith("_") and p.stem != "catalog"
)

TEST_HEADER = "#### 🧪 自测用例"
REF_HEADER = "### 参考实现"
REF_END = "### 这个模式还出现在……"

PY_BLOCK = re.compile(r"```python\n(.*?)```", flags=re.DOTALL)


def extract_python(text: str) -> list[str]:
    return PY_BLOCK.findall(text)


def run_card(name: str) -> None:
    path = PATTERNS / f"{name}.md"
    text = path.read_text(encoding="utf-8")

    # 自测用例：从「🧪 自测用例」到「### 参考实现」
    t0 = text.index(TEST_HEADER)
    t1 = text.index(REF_HEADER, t0)
    test_code = "\n".join(extract_python(text[t0:t1]))

    # 参考实现：从「### 参考实现」到「### 这个模式还出现在……」
    r0 = text.index(REF_HEADER)
    r1 = text.index(REF_END, r0)
    ref_code = "\n".join(extract_python(text[r0:r1]))

    full = f"{ref_code}\n\n{test_code}"

    ns = {"__name__": "selfcheck"}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(compile(full, str(path), "exec"), ns)
    except AssertionError as exc:
        print(f"❌ {name}: 断言失败 {exc}")
        return False
    except Exception as exc:  # noqa: BLE001
        print(f"❌ {name}: {type(exc).__name__}: {exc}")
        return False

    print(f"✅ {name}")
    return True


def check_links() -> bool:
    """检查仓库内所有 .md 的内部相对链接是否指向存在的文件。"""
    root = Path(__file__).resolve().parent.parent
    ok = True
    for md in sorted(root.rglob("*.md")):
        base = md.parent
        text = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\]\(([^)]+\.md)\)", text):
            target = (base / m.group(1)).resolve()
            if not target.is_file():
                print(f"❌ 死链: {md.relative_to(root)} → {m.group(1)}")
                ok = False
    if ok:
        print("✅ 内部链接全部有效")
    return ok


def main() -> int:
    results = {name: run_card(name) for name in CARDS}
    passed = sum(results.values())
    links_ok = check_links()
    print(f"\n通过 {passed}/{len(CARDS)} 张卡")
    return 0 if passed == len(CARDS) and links_ok else 1


if __name__ == "__main__":
    sys.exit(main())
