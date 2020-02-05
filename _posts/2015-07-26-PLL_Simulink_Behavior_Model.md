---
layout:     post
title:      "PLL Simulink行为模型"
date:       2015-07-26 22:37:38
author:     "MaZhaoxin"
header-img: "img/bg-post/pll.jpg"
catalog:    true
tags:
    - PLL
    - MATLAB
---

## VCO
根据配置的参数计算当前的频率，然后进行循环积分，然后转成方波输出。
![](/img/in-post/{{page.id | replace:'/','-'}}/VCO.png)

## NDIV
主要由两个triggered subsysterm组成，分别是prescaler和PSC，注意由于存在收敛性问题，需要把input的`Latch input by delaying outside signal`选项勾上。
![](/img/in-post/{{page.id | replace:'/','-'}}/NDIV.png)

## SDM
对于这种本身就是数字时序电路的模块来说，最简单的办法就是直接用triggered subsystem搭出来。
![](/img/in-post/{{page.id | replace:'/','-'}}/SDM.png)

## PD
PD就是个异或门，但需要将输出转为double型，以和LPF进行匹配。
![](/img/in-post/{{page.id | replace:'/','-'}}/PD.png)

## PFD
用带enable的triggered subsystem实现DFF的功能，然后按照正常的实现方式搭出来就可以了。
![](/img/in-post/{{page.id | replace:'/','-'}}/PFD.png)

## CP
CP的功能是把输入的电压脉冲转换成电流脉冲，简单的结构如下，顺便加入了offset功能。
![](/img/in-post/{{page.id | replace:'/','-'}}/CP.png)

## LPF
需要根据零极点对增益g进行调整。
![](/img/in-post/{{page.id | replace:'/','-'}}/LPF.png)

## LO
为了输出50%的占空比信号，用double edge triggered subsystem来做。
![](/img/in-post/{{page.id | replace:'/','-'}}/LO.png)
