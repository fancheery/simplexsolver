"""从零实现的单纯形法求解器。

支持标准形线性规划：

    max   c^T x
    s.t.  A x <= b
          x >= 0

其中 b >= 0（b 为负需要用两阶段法，见 README 的 TODO）。

用法：
    from simplex import solve_lp
    x, obj, status = solve_lp(c, A, b)
"""

from __future__ import annotations

import numpy as np

EPS = 1e-9


def solve_lp(c, A, b, verbose=False, max_iter=1000):
    """求解标准形 LP。

    参数
    ----
    c : (n,) 目标函数系数，求最大化
    A : (m, n) 约束矩阵
    b : (m,) 右端项，必须 >= 0
    verbose : 是否打印每一步迭代

    返回
    ----
    (x, obj, status)
        x      : 最优解向量；无界或失败时为 None
        obj    : 最优目标值
        status : "optimal" / "unbounded" / "max_iter_reached"
    """
    c = np.asarray(c, dtype=float)
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)

    if A.ndim != 2:
        raise ValueError("A 必须是二维矩阵")
    m, n = A.shape
    if c.shape != (n,):
        raise ValueError(f"c 的长度应为 {n}，实际是 {c.shape}")
    if b.shape != (m,):
        raise ValueError(f"b 的长度应为 {m}，实际是 {b.shape}")
    if np.any(b < -EPS):
        raise ValueError("当前实现要求 b >= 0；b 为负需用两阶段法（见 README TODO）")

    # 单纯形表：m 行约束 + 1 行目标函数
    # 列 = n 个决策变量 + m 个松弛变量 + 1 列右端项
    T = np.zeros((m + 1, n + m + 1))
    T[:m, :n] = A
    T[:m, n : n + m] = np.eye(m)   # 松弛变量，初始基
    T[:m, -1] = b
    T[-1, :n] = -c                  # 目标函数行（最大化写成负号）

    basis = list(range(n, n + m))   # 初始基变量：全部是松弛变量

    if verbose:
        print(f"初始：基变量 = {[_name(i, n) for i in basis]}，目标值 = {T[-1, -1]:.4f}")
        print()

    for step in range(1, max_iter + 1):
        # 1) 选换入变量：目标行里最负的那一列
        reduced = T[-1, :-1]
        j = int(np.argmin(reduced))
        if reduced[j] >= -EPS:
            x = _extract(T, basis, n)
            return x, float(T[-1, -1]), "optimal"

        # 2) 比值检验，选换出变量
        col = T[:m, j]
        rows = np.where(col > EPS)[0]
        if rows.size == 0:
            return None, float("inf"), "unbounded"
        r = int(rows[np.argmin(T[rows, -1] / col[rows])])
        leaving = basis[r]

        # 3) 主元消去
        T[r] /= T[r, j]
        for i in range(m + 1):
            if i != r and abs(T[i, j]) > EPS:
                T[i] -= T[i, j] * T[r]
        basis[r] = j

        if verbose:
            x = _extract(T, basis, n)
            print(
                f"第 {step} 步：换入 {_name(j, n)}，换出 {_name(leaving, n)}"
                f" → 目标值 = {T[-1, -1]:.4f}，解 = {np.round(x, 4)}"
            )

    return None, float("nan"), "max_iter_reached"


def _extract(T, basis, n):
    """从单纯形表读出当前的基本可行解。"""
    x = np.zeros(n)
    for i, bi in enumerate(basis):
        if bi < n:
            x[bi] = T[i, -1]
    return x


def _name(idx, n):
    """把列下标翻译成人看得懂的名字。"""
    return f"x{idx + 1}" if idx < n else f"s{idx - n + 1}"


if __name__ == "__main__":
    print("求解这道线性规划：")
    print("    max  3*x1 + 5*x2")
    print("    s.t. 3*x1 + 2*x2 <= 18")
    print("         x1 <= 4")
    print("         x2 <= 6")
    print("         x1, x2 >= 0")
    print()
    print("-" * 60)

    x, obj, status = solve_lp(
        c=[3, 5],
        A=[[3, 2], [1, 0], [0, 1]],
        b=[18, 4, 6],
        verbose=True,
    )

    print("-" * 60)
    print(f"状态    ：{status}")
    if x is not None:
        print(f"最优解  ：x1 = {x[0]:.4f}, x2 = {x[1]:.4f}")
        print(f"最优值  ：{obj:.4f}")
    print()
    print("理论答案是 x1=2, x2=6, 最优值 36。对上了就说明算法是对的。")
