"""simplex.py 的单元测试。

运行：
    python -m pytest -q
"""

import pytest

from simplex import solve_lp


def test_demo_problem():
    """README 里的例子，理论最优 x1=2, x2=6, 值 36。"""
    x, obj, status = solve_lp([3, 5], [[3, 2], [1, 0], [0, 1]], [18, 4, 6])
    assert status == "optimal"
    assert obj == pytest.approx(36.0)
    assert x[0] == pytest.approx(2.0)
    assert x[1] == pytest.approx(6.0)


def test_single_variable():
    """最简单的情况：max x, s.t. x <= 5。"""
    x, obj, status = solve_lp([1], [[1]], [5])
    assert status == "optimal"
    assert obj == pytest.approx(5.0)
    assert x[0] == pytest.approx(5.0)


def test_unbounded():
    """max x1 + x2 在 x>=0 上没有上界，应该被识别为无界。"""
    x, obj, status = solve_lp([1, 1], [[-1, 0], [0, -1]], [0, 0])
    assert status == "unbounded"
    assert x is None


def test_negative_b_rejected():
    """b 为负时当前实现应明确报错，而不是给出错误结果。"""
    with pytest.raises(ValueError):
        solve_lp([1], [[1]], [-1])
