---
layout:     post
title:      "理想倍频器/分频器对相噪/杂散的影响"
date:       2015-07-26 23:02:40
author:     "MaZhaoxin"
header-img: "img/bg-post/pll.jpg"
catalog:    true
tags:
    - PLL
typora-root-url:	..
---

### 结论
使用理想倍频器将信号频率提高 $N$ 倍，会让相噪抬高$20log_{10}(N)$dB，类似的$N$分频会让相噪降低$20log_{10}(N)$dB。

### 理想倍频器
对于信号 $f(t) = cos(\omega t + \phi(t))$，倍频器的功能是把$cos$函数的参数（相位）增大$N$倍，即任何相位域的噪声都会放大$N$倍，即相位噪声抬高$20log_{10}(N)$dB。

而对于调频信号（杂散） $f(t) = cos(\omega_{c} t + \beta sin(\omega_{m} t))$，对于较小的$\beta$则有
$$
f(t) = cos(\omega_{c} t) + (\beta/2)*[cos(\omega_{c} - \omega_{m}) t - cos(\omega_{c} + \omega_{m}) t]
$$
若该信号经过$N$倍频器变成 $f(t) = cos(N \omega_{c} t + N \beta sin(\omega_{c} t))$，同样对于较小的$N \beta $则有
$$
f(t) = cos(N \omega_{c} t) + (N \beta/2)*[cos(\omega_{c} - \omega_{m}) t - cos(\omega_{c} + \omega_{m}) t]
$$
即边带幅度增大了 $20log_{10}(N)$dB，且频偏与原信号相同。

### 理想分频器
与前面类似的推导方法，可得经过N分频器后相位噪声降低 $20log_{10}(N)$dB，边带幅度同样降低$20log_{10}(N)$dB，频偏与原信号相同。

-------------------------------------------------------------

**参考**：http://www.ko4bb.com/~bruce/IdealFreqMultDiv.html
