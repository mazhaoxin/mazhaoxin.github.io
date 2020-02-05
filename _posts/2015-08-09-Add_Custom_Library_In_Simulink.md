---
layout:     post
title:      "在Simulink中创建自己的Library"
date:       2015-08-09 23:46:17  
author:     "MaZhaoxin"
header-img: "img/bg-post/matlab.jpg"
catalog:    true
tags:
    - MATLAB
---

[前面](/{{ "2015-07-26-PLL_Simulink_Behavior_Model" | replace:'-','/' }})说了一些常用的PLL行为模型，为了方便后续的调用，可以在simulink中创建个library进行管理。

步骤如下：

1. 新建library。
    ![](/img/in-post/{{page.id | replace:'/','-'}}/Step1.png)

2. 把封装好的subsystem复制到新的library中，并保存。此时各模块的属性就是从browser中调用时的默认属性。
    ![](/img/in-post/{{page.id | replace:'/','-'}}/Step2.png)

3. 在.mdl文件同目录下创建名为`blkStruct.m`的函数，内容如下所示。其中第3行定义了.mdl的文件名，第4行定义了在browser中的显示名（这里为了让自定义的library排在前面加了下划线的前缀），第5行说明是否含有下一层目录。
    ```matlab
    function blkStruct = slblocks
    
    Browser(1).Library = 'CustomLib';
    Browser(1).Name    = '__Custom Library';
    Browser(1).IsFlat  = 1; % Is this library "flat" (i.e. no subsystems)?
    
    blkStruct.Browser = Browser;
    ```

4. 将.mdl文件所在的目录添加到path中。
  ![](/img/in-post/{{page.id | replace:'/','-'}}/Step4.png)

5. 重新打开simulink library browser就可以看到添加的library了。
  ![](/img/in-post/{{page.id | replace:'/','-'}}/Step5.png)
