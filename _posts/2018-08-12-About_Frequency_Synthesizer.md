---
layout:     post
title:      "关于频率综合器"
date:       2018-08-12 23:11
author:     "MaZhaoxin"
header-img: "img/bg-post/pll.jpg"
catalog:    true
tags:
    - PLL
typora-root-url:	..
---

> 前几天在饭桌上老大突然问了一个问题：DDS中的“S”为什么叫“综合器”？

## 命名

好像大家都把`Frequency Synthesizer`翻译为“频率综合器”，但为啥呢？另外，为啥这么一个模块，大家都叫它为`Synthesizer`？

`synthesize`的名词形式是`synthesis`，根据[youdict](http://www.youdict.com/w/synthesis)上的说明，它是由`syn-`（一起）和`-thes`（做，同do）组合在一起的，本意是`一起做什么事`，引申为`合成`，在化学上用的比较多。网上有张图片看着不错，放在了下面。

![](/img/in-post/2018-08-12-About_Frequency_Synthesizer.assets/Synthesizing_word.jpg)

所以说，Digital IC Design Flow中的`synthesize`这步的名称看起来是非常合理的。它所做的操作是把RTL code转换成了由stdcell组成的netlist，也就是说把很多个stdcell（小片的东西）放在一起，让它们体现出了某种逻辑（行为）。这与化学上的合成非常类似，就像把很多个氨基酸放在一起，它们就体现为了具有某种功能的蛋白质。

但用这个来解释”频率综合器“好像还是不妥，再接着看引申义。`synthesizer`通常的含义是电子音合成器，就是把声音相叠加、调制来*制造*（合成）音乐的东西。这是对声波的进阶使用，可以通过叠加不同权重、不同频率的单音（逆傅立叶变换），也可以通过混频、调频来实现。看起来这个就与我们所说的`Frequency Synthesizer`的含义比较接近了。

[Wikipedia](https://en.wikipedia.org/wiki/Frequency_synthesizer)上关于`Frequency Synthesizer`的定义和说明是：

> A frequency synthesizer is an electronic circuit that generates a range of frequencies from a single reference frequency. ... A frequency synthesizer may use the techniques of frequency multiplication, frequency division, direct digital synthesis, frequency mixing, and phase-locked loops to generate its frequencies.

从定义来看，它有3个要素，分别是电路、输入单一频率、输出一定范围的频率。从功能上来看，能输出一定范围的频率就与电子音合成器那个生成不同频率（音调）的声音相同了。

综上，**我觉得**产生一定范围频率的信号的模块叫做`Frequency Synthesizer`是借用了电子音合成器的名字（未严谨考究，可能存在误差），而翻译成中文更准确的名字应当是”频率合成器“，不知道是否是因为”频率综合器“的简称”频综“更上口一些，还是有其他的原因，”频率综合器“的命名就一直流传了下来。

## 实现

如果只写前面这种不严谨且没啥鸟用的命名考究的话，实在是太过无聊了些，那就说说实现吧。

如前面Wikipedia的说明所讲，频综在实现上会用到很多技术，如倍频、除频、直接数字合成、混频和锁相环。

其中除了混频利用了真正意义上的频率域原理，其余的均与`沿`有关，并且分成开环与闭环两种模式。

### 开环结构

所谓开环，顾名思义，即是不对输出信号做任何检测，靠系统原理保证输出信号的正确性。

比如除频的方式（*别不把分频器当频综*），由输入时钟信号的沿触发，通过寄存器存储沿的个数，当个数达到一定值时清空寄存器并产生一个沿，周而复始。那么首先输出信号的沿出现的时刻必定与输入信号的某个沿相关。单纯的除频由于不能产生除了输入信号的沿以外的`时刻`，因此它的输出频率必定是受输入信号约束的。

![](/img/in-post/2018-08-12-About_Frequency_Synthesizer.assets/Divider.png)

如上图所示的除10分频器时序图，输出信号反转（产生上升沿或下降沿）的时刻一定对应了输入信号的相应的上升沿。因此，**单沿触发的分频器不可能实现占空比为50%的奇数分频比**。

### 开环结构的进阶

由于除频的方式不能产生新的`沿`的约束，在实际应用中除频的方法受到了很多限制，那么能不能突破这个限制呢？

如果要突破这个限制就要想办法产生新的`沿`，而在电路中最简单的产生新的`沿`的方式是**延时**。

下图所示的是一种基于DTC（数字时间转换器）的小数分频器（Frac-N Divider）的时序图，所示的分频比为4.75。

![](/img/in-post/2018-08-12-About_Frequency_Synthesizer.assets/FracN_Divider.png)

显然分频比的步长越小，对DTC的要求就越高。

### 剑走偏锋的开环结构

直接数字合成（DDS）所用的方法相对特殊一些，其框图（参考自[Wikipedia](https://en.wikipedia.org/wiki/Direct_digital_synthesis)）如下所示，它首先在数字域产生了波形，然后通过DAC将其转换到模拟域，再通过滤波器滤除无用的镜像信号，即可获得想要的波形。由于数字域的灵活性，该方式几乎可以实现任意的波形，所以在函数信号发生器中有广泛应用。但由于实现的复杂度高、难以产生低噪声（抖动）的时钟信号，在现代通信电路和时钟产生器中并不多见。

![](/img/in-post/2018-08-12-About_Frequency_Synthesizer.assets/DDS.png)

### 闭环形式

从前面的演化也能看出，如果能有个自由的`沿`产生模块，频综的输出频率会自在很多。而这个模块即是——振荡器。

但自由的缺点就是如果不管它，它的输出频率会出现漂移，这个时候就需要一个环路把它给矫正回来。

根据闭环自动控制系统的结构，环路中最重要的是执行器、被控对象和检测装置组成，其中被控对象显然是振荡器，而执行器则通常由环路滤波器担任。

- 如果将计数器作为检测装置，通过对比当前输出频率与目标输出频率的差，来调节振荡器的控制信号，这则是锁频环（FLL）。
- 如果将输出信号的沿与参考信号的沿（相位）之间的超前滞后情况检测出来，作为调节振荡器的依据，这则是锁相环（PLL）。

在闭环自动控制系统中，真正对输出信号起控制作用的是偏差信号，而FLL和PLL的本质区别在于偏差信号是频率还是相位，与滤波器的特性无关。并且在分析Bogdan架构的ADPLL时，我们可以看到二者是殊途同归的，这个以后再展开详述。

## 总结

频综只是频率合成器的一个叫法罢了，反正能产生想要的频率就行了。至于怎么产生，是乘、是除、还是自己造那都是实现的事了。