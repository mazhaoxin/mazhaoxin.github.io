---
layout:     post
title:      "由相位噪声曲线计算积分相噪和Jitter的方法"
date:       2015-08-09 23:03:46 
author:     "MaZhaoxin"
header-img: "img/bg-post/pll.jpg"
catalog:    true
tags:
    - PLL
typora-root-url:	..
---

先放一张忘了从哪扒下来的图：
![](/img/in-post/2015-08-09-Calculate_IPN_Jitter_Based_On_Phase_Noise.assets/pn.png)
> Update @20240509
> 
> Ref: [https://www.analog.com/media/en/training-seminars/tutorials/MT-008.pdf](https://www.analog.com/media/en/training-seminars/tutorials/MT-008.pdf)

**基本思路**：
分段求积分相噪，相加得整体的积分相噪，进而得到以弧度为单位的相位抖动，最终转换为以时间为单位的Jitter。

**MATLAB代码**：
```MATLAB
function ph2jt(fc, f, ph)
	% ph2jt(fc, f, ph) 
	% fc - carrier frequency 
	% f - offset frequency 
	% ph - phase noise at offset frequency 
	N = length(f); 
	if(ph(1) > 0) 
		for i=1:N 
			ph(i) = -ph(i); 
		end 
	end 
	a = zeros(1, N-1); 
	a_dBc = zeros(1, N-1); 
	jt = zeros(1, N-1); 
	for i=2:N 
		f0 = f(i-1); 
		f1 = f(i); 
		ph0= 10^(ph(i-1)/10); 
		ph1= 10^(ph(i)/10); 
		k = 10*log10(ph1/ph0)/log10(f1/f0); 
		a(i-1) = 10*f1*ph0*(f1/f0)^(k/10)/(10+k) - 10*f0*ph0/(10+k); 
		a_dBc(i-1) = 10*log10(a(i-1)); 
		jt(i-1) = sqrt(2*a(i-1))/(2*pi*fc); 
	end 
	a_tol = sum(a); 
	a_tol_dBc = 10*log10(a_tol); 
	jt_tol = sqrt(2*a_tol)/(2*pi*fc); 
	for i=1:N-1 
		display(sprintf('%g ~ %g\t%g\t%f\t%g', f(i), f(i+1), a(i), a_dBc(i), jt(i))); 
	end 

	display(sprintf('Total\t\t%g\t%f\t%g', a_tol, a_tol_dBc, jt_tol)); 
```
