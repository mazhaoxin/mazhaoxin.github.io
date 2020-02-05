---
layout:     post
title:      "Matlab符号运算"
date:       2013-09-07 23:03:54
author:     "MaZhaoxin"
header-img: "img/bg-post/matlab.jpg"
catalog:    true
tags:
    - MATLAB
---

##### 一、声明

> 声明单个符号变量：sym('a')
>
> 声明多个符号变量：syms a b c

##### 二、符号表达式

> 提取分子分母：[n,d]=numdem(a)
>
> 自变量为v的符号函数的反函数：finverse(f,v)
>
> 求和  ：symsum(s,v,a,b)

##### 三、符号表达式化简

> 以直观漂亮的形式显示：pretty(f)
>
> 合并同类项：collect(f)
>
> 因式分解：factor(f)
>
> 展开：expand(f)
>
> 化简（显示最短）：simplify(f)
>
> 同时尝试多种化简方法：simple(f)
>
> 分离分子分母：[num, den] = numden(f)
>
> 符号多项式转矩阵：sym2poly(f)
>
> 表达式代入数值：subs(f, {x1,x2,…}, {1,2,…})

##### 四、符号矩阵

> 转置：transpose(A)
>
> 求行列式：det(A)
>
> 求逆：inv(A)
>
> 求秩：rank(A)

##### 五、符号微积分

> 极限  ：limit(f,x,a)
>
> 微分：diff(f,'a',n)
>
> 积分：int(f,v,a,b)

##### 六、符号函数画图

> 绘图：ezplot(f,[a,b])

##### 七、符号方程求解

> 求解线性方程：solve(f)
>
> 求解非线性方程：fsolve(fun,x0)
>
> 求解微分方程：dsolve('eqn1','eqn2',…)

\* 在Help中搜索`Symbolic Math Toolbox`可以查看相关Manual。

