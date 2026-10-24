r"""交互式线性规划求解器：你输入数据，它给出最优解。

两种用法：

1. 交互输入（一步一步问你）
       python run.py

2. 从 JSON 文件读
       python run.py 题目.json

   文件格式：
       {
         "c": [3, 5],
         "A": [[3, 2], [1, 0], [0, 1]],
         "b": [18, 4, 6]
       }
"""

from __future__ import annotations

import json
import sys

from simplex import solve_lp


def parse_floats(text: str, count: int, name: str) -> list[float]:
    """把 '3 2' 这类输入解析成 [3.0, 2.0]，并检查个数。"""
    parts = text.replace(",", " ").replace("，", " ").split()
    if len(parts) != count:
        raise ValueError(f"{name} 需要 {count} 个数，你给了 {len(parts)} 个：{text!r}")
    return [float(p) for p in parts]


def show_problem(c, A, b) -> None:
    """把 c/A/b 还原成数学写法，让用户确认没输错。"""
    n = len(c)
    print("你输入的问题是：")
    print("  max  " + " + ".join(f"{v:g}*x{i + 1}" for i, v in enumerate(c)))
    for i, row in enumerate(A):
        lhs = " + ".join(f"{v:g}*x{j + 1}" for j, v in enumerate(row))
        print(f"  s.t. {lhs} <= {b[i]:g}")
    print("       " + ", ".join(f"x{i + 1}" for i in range(n)) + " >= 0")
    print()


def show_result(c, A, b) -> None:
    """求解并用人话打印结果。"""
    try:
        x, obj, status = solve_lp(c, A, b)
    except ValueError as e:
        print(f"无法求解：{e}")
        return

    if status == "optimal":
        print("最优解：")
        for i, v in enumerate(x):
            print(f"  x{i + 1} = {v:.4f}")
        print(f"最优值：{obj:.4f}")
        print()
        print("各约束的使用情况：")
        for i, row in enumerate(A):
            used = sum(a * xi for a, xi in zip(row, x))
            slack = b[i] - used
            tag = "（正好用满，是瓶颈）" if abs(slack) < 1e-6 else f"（还剩 {slack:.4f}）"
            print(f"  约束 {i + 1}: {used:.4f} <= {b[i]:g} {tag}")
    elif status == "unbounded":
        print("这个问题没有最优解：目标函数可以无限增大（无界）。")
        print("通常意味着少了约束，或者把不等号方向写反了。")
    else:
        print(f"求解失败，状态：{status}")


def interactive() -> None:
    print("=" * 55)
    print("线性规划求解器")
    print("=" * 55)
    print("能解这种形式：")
    print("   max  c1*x1 + c2*x2 + ...")
    print("   s.t. a1*x1 + a2*x2 + ... <= b")
    print("        x >= 0")
    print()
    print("（按 Ctrl+C 可随时退出）")
    print()

    try:
        n = int(input("变量个数 n = ").strip())
        c = parse_floats(input(f"目标函数系数 c（{n} 个数，空格分隔）= "), n, "c")

        m = int(input("约束个数 m = ").strip())
        A: list[list[float]] = []
        b: list[float] = []
        for i in range(m):
            row = parse_floats(
                input(f"  约束 {i + 1} 的系数（{n} 个数）= "), n, f"约束 {i + 1} 的系数"
            )
            rhs = float(input(f"  约束 {i + 1} 的右端 b = ").strip())
            A.append(row)
            b.append(rhs)
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        return
    except ValueError as e:
        print(f"\n输入有误：{e}")
        return

    print()
    show_problem(c, A, b)
    show_result(c, A, b)


def from_file(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    c, A, b = data["c"], data["A"], data["b"]
    show_problem(c, A, b)
    show_result(c, A, b)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        from_file(sys.argv[1])
    else:
        interactive()
