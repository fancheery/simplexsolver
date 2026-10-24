# simplex-solver

从零实现的**线性规划（LP）求解器**，核心算法是单纯形法（Simplex Method）。

不调用任何现成求解器——`numpy` 只用来做矩阵运算，算法本身是自己写的。

## 它解决什么问题

线性规划就是在一组线性约束围出的范围里，找一个点让线性目标最大：

```
max   c^T x
s.t.  A x <= b
      x >= 0
```

举个具体例子：

```
max  3*x1 + 5*x2
s.t. 3*x1 + 2*x2 <= 18
      x1 <= 4
      x2 <= 6
      x1, x2 >= 0
```

可行域是一个五边形，最优解一定在某个顶点上。单纯形法从一个顶点出发，
每次沿边走一步、换到更优的相邻顶点，直到走不动为止。

## 快速开始

需要 Python 3.10+。**第一次运行先建环境：**

```powershell
cd C:\dev\simplexsolver
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

之后每次运行：

```powershell
.\.venv\Scripts\activate
python simplex.py
```

输出：

```
求解这道线性规划：
    max  3*x1 + 5*x2
    ...
初始：基变量 = ['s1', 's2', 's3']，目标值 = 0.0000

第 1 步：换入 x2，换出 s3 → 目标值 = 30.0000，解 = [0. 6.]
第 2 步：换入 x1，换出 s2 → 目标值 = 36.0000，解 = [2. 6.]

状态    ：optimal
最优解  ：x1 = 2.0000, x2 = 6.0000
最优值  ：36.0000
```

跑测试：

```powershell
python -m pytest -q
```

## 项目结构

```
simplexsolver/
├── simplex.py         # 核心算法 + 演示
├── test_simplex.py    # 单元测试
├── requirements.txt
└── README.md
```

## 现在的局限（这就是你的任务清单）

当前版本只能处理 `b >= 0` 的标准形，还有很多没做。**按顺序往下做，每完成一项就提交一次：**

- [ ] **两阶段法**：允许 `b` 为负（需要先构造辅助问题求初始可行解）
- [ ] **Bland 规则**：防止退化情形下无限循环
- [ ] **对偶单纯形法**：支持灵敏度分析
- [ ] **算例对比**：在 [netlib LP](https://www.netlib.org/lp/) 上跑标准算例，与 HiGHS 对比求解时间和迭代次数
- [ ] **稀疏矩阵**：大算例用 `scipy.sparse` 存表，避免内存爆炸
- [ ] **等式约束**：支持 `A x = b`
- [ ] **更好的可视化**：画出二维问题的可行域和迭代路径

## 参考与致谢

- 算法理论：Dantzig, G. B. (1963). *Linear Programming and Extensions*
- 教材：Boyd & Vandenberghe, *Convex Optimization*, Ch. 4
- 算例来源：[netlib LP](https://www.netlib.org/lp/)
- 本实现为独立编写，未复制其他项目代码

## License

MIT
