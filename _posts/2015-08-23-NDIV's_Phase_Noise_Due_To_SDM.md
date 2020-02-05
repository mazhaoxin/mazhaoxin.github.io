---
layout:     post
title:      "SDM对分频器输出信号相位噪声的影响"
date:       2015-08-23 23:04:03
author:     "MaZhaoxin"
header-img: "img/bg-post/pll.jpg"
catalog:    true
tags:
    - PLL
---

SDM是PLL里很重要的一个噪声源，下面分析一下SDM对NDIV输出时钟相噪的影响。

![](/img/in-post/{{page.id | replace:'/','-'}}/diagram.png)

首先，SDM输出信号的噪声是量化噪声的$sdm\_order$次差分（具体推导暂且不提），而量化噪声是在$[-fclk , +fclk]$范围内**均匀分布**，噪声功率为$\Delta^2/12$，差分的传函是$1-z^{-1}$，则有
$$
PSD_{SDM} = Qn*((1-z^{-1})^{sdm\_order})^2 = (1/12/fclk)*((1-z^{-1})^3)^2
$$
其中，$fclk = fref$。

然后，对于分频比序列$n[i]$，NDIV输出信号的上升沿位于
$$
t[i] = t_0+\sum_i (n[i] *Tvco) = t_0+\sum_i((n_{avg}+n_{err}[i])*Tvco) = t_0+i*Tref+Tvco*\sum_i n_{err}[i]
$$

由此可得NDIV输出信号的相位误差为
$$
ph_{err}[i] = 2\pi/n_{avg}*\sum_i n_{err}[i]
$$

由上式可以看到SDM的噪声到NDIV的输出端有个累加过程，累加的传函是$1/(1-z^{-1})$，即抵消掉SDM的一个差分。

综上，NDIV输出的相位噪声为
$$
PN_{NDIV} = (1/12/fref)*((1-z^{-1})^{(sdm\_oder-1)})^2*(2\pi/n_{avg})^2
$$

最后放上理论值与仿真结果的对照：
![](/img/in-post/{{page.id | replace:'/','-'}}/results.png)

*注：此处的仿真结果为`two-sided PSD`。
