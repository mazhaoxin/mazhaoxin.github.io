---
layout: post
title: "markdown中的latex公式"
date: 2022-05-09 22:13
author: "MaZhaoxin"
header-img: "img/bg-post/coding.jpg"
catlog: true
tags:
      - Programing
typora-root-url:	..
---

> 喜欢markdown的很重要一点就是能用latex语法写数学公式，而不用安装那庞大的latex环境。但是markdown和latex毕竟“每个人有他的脾气”，所以“相爱没有那么容易”。把一些经验和总结记录下来，已被不时之需。

### 基本规则

行内时使用两个单美元符号标记（`$...$`），单独行时使用两个双美元符号标记（`$$...$$`），例如：

- 行内的例子（`$x+y=z$`）：$x+y=z$ 

- 单独成行的例子（`$$回车x+y=z回车$$`）：
  $$
  x+y=z
  $$

如果需要使用美元符号，不希望被误识别成公式，则要在前面加反斜杠，即`\$`。

### 希腊字母（Greek Alphabet）

在24个希腊字母中，latex支持30个小写字母（包括6个变体写法）和11个大写字母。使用方法非常简单，用`反斜杠+字母英文名`表示即可，其中字母英文名全小写表示小写希腊字母，首字母大写则表示大写希腊字母。例如：

- `\alpha`：$\alpha$，`\delta`：$\delta$
- `\Delta`：$\Delta$

![greek_aphabet](/img/in-post/2022-05-09-latex_in_markdown.assets/greek_letters.jpg)

### 角标

角标的表示同样非常简单，下标用"_"，上标用“^”，若角标的内容超过一个字符则需要用花括号引起来。如果同时存在上下角标可以依次表示，顺序不重要。例如：

- `x^2`：$x^2$，`e^{j \omega t}`：$e^{j\omega t}$
- `x_1`：$x_1$，`x_1^2`：$x_1^2$

### 分数

分数有两种表示方法，其一是直接用斜杠表示，另外一种是用`\frac{num}{den}`格式。例如：

- `(a+1)/(b+1)`：$(a+1)/(b+1)$
- `\frac{a+1}{b+1}`：$\frac{a+1}{b+1}$

### 根号

平方根的表示方法为`\sqrt{x}`，若要表示n次根号下，则需要添加方括号标记（`\sqrt[n]{x}`）。例如：

- `\sqrt{x^2+1}`：$\sqrt{x^2+1}$
- `\sqrt[3]{x^2+1}`：$\sqrt[3]{x^2+1}$

### 积分、累加符号

积分符号可以直接用`\int`调出来，然后通过角标加积分范围，被积分的内容直接写在后面即可。类似的还有累加符号，可以用`\sum`调出来。例如：

- `\int_1^2 x dx`：$\int_1^2 x dx$
- `\sum_1^2 n`：$\sum_1^2 n$

注意，微分符号“d“是以斜体表示的，如果想改为正体需要用到`\mathrm{}`，即

- `\int_1^2 x \mathrm{d} x`：$\int_1^2 x \mathrm{d} x$

从中可以看出来，空格在latex公式中是被忽略的，因此大可放心的使用空格增强可读性。

### 括号、绝对值符号

一般情况下，括号直接输入即可，绝对值符号也可以用反斜杠上面的那个（`|`），但这样的缺点是括号高度不会跟着内容变化，解决办法是用`\left`、`\right`进行标记。对比一下这两种写法：

- `( \frac{\frac{a}{b}}{\frac{c}{d}} )`：$( \frac{\frac{a}{b}}{\frac{c}{d}} )$
- `\left( \frac{\frac{a}{b}}{\frac{c}{d}} \right)`：$\left( \frac{\frac{a}{b}}{\frac{c}{d}} \right)$

### 常用符号

有时候我们还会用到一些特殊符号，比如点乘号、正负号、大于等于、远大于、约等于、箭头等等，均可以用“反斜杠+符号名”的方式表示，当然前提是得知道符号名。常用的有：

- `\cdot`：$\cdot$（点乘号），`\times`：$\times$（叉乘号），`\div`：$\div$
- `\pm`：$\pm$，`\approx`：$\approx$
- `\le`：$\le$，`\ge`：$\ge$，`\ll`：$\ll$，`\gg`：$\gg$（`l`表示less，`g`表示greater，`e`表示equal）
- `\to`：$\to$，`\downarrow`：$\downarrow$，`\uparrow`：$\uparrow$

更多的可参考latex的文档，也可以使用在线编辑器查找，这里推荐“妈咪说”的[https://www.latexlive.com/](https://www.latexlive.com/)。

### 常用函数

因为latex在渲染公式时默认使用斜体，但对于一些函数名则可以通过在前面加反斜杠使其变成正体。对比一下这两种写法：

- `sin(x)`：$sin(x)$，`sin^{-1}(x)`：$sin^{-1}(x)$
- `\sin(x)`：$\sin(x)$，`\sin^{-1}(x)`：$\sin^{-1}(x)$

类似的还有`cos`、`tan`、`ln`、`log`等。

### 正体、斜体与花体

如前面提到的，latex在渲染时默认使用斜体，如果想改为正体需要用`\mathrm{}`标记，如果想改为花体则需要用`\mathcal{}`标记。例如：

- `L(f)`：$L(f)$
- `\mathrm{L}(f)`：$\mathrm{L}(f)$
- `\mathcal{L}(f)`：$\mathcal{L}(f)$ ——常用这个标记代表相位噪声

### 方程式组、多行等式

当使用方程式组或者多行等式时，出于美观的考虑，我们希望等号是上下对齐的，这个时候需要用到`eqnarray`环境，具体的用法如示例：

```latex
\begin{eqnarray}
a &=& b+c+d \\
c+d &=& e+f+g+h \\
&>& i+j
\end{eqnarray}
```

$$
\begin{eqnarray}
a &=& b+c+d \\
c+d &=& e+f+g+h \\
&>& i+j
\end{eqnarray}
$$

不难看出，有3个要点：

1. 用`\begin{eqnarray}`和`\end{eqnarray}`把需要对齐的部分括起来；
2. 需要对齐的部分用`&`括起来；
3. 行尾需要加`\\`。

### 与markdown的冲突和解决方法

markdown本身就是一种标记语言，有时候不小心就会出现误识别的现象（如`$`符号），一般可以用反斜杠`\`解决，例如（可能是mathjax的bug，在Typora中显示正常）：

- `\mathcal{L}_{b}=\mathcal{L}_{b}`：$\mathcal{L}_{b}=\mathcal{L}_{b}$
- `\mathcal{L}\_{b}=\mathcal{L}\_{b}`：$\mathcal{L}\_{b}=\mathcal{L}\_{b}$

还有绝对值符号引起的错误（被误识别成表格），则需要把`|`换成`\vert`来解决，例如：

- `|H(s)|`：$|H(s)|$

- `\vert H(s) \vert`：$\vert H(s) \vert$

如果想输出latex公式的源代码，用反引号标记的代码模式是最方便的，比如：

- `\\\$`：\\\$
- \`\\\\$\`：`\$`

> 后记：当年硕士答辩时，被答辩老师吐槽论文里的公式是用Word自带的公式编辑器写的，很丑。多年以后，我只想说——老师说的对啊！