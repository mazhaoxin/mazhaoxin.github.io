---
layout:     post
title:      "美化Cadence Library Manager"
date:       2019-01-09 21:10
author:     "MaZhaoxin"
header-img: "img/bg-post/manager.jpg"
catalog:    true
tags:
    - Cadence
    - Manager
typora-root-url:	..
---

俗话说“工欲善其事，必先利其器”，如果能让工作环境更整洁、用起来更顺手，那么工作效率必然也会高一些。

在实际项目中经常会遇到`cds.lib`里关联了一堆lib，包括

- foundary提供的各种版本的stdcell
- 公司内部的基本库
- 当前项目的lib
- 参考项目的lib
- Testbench lib等等

有时候在浩瀚的左侧列表中寻找所需的lib着实是需要费一番功夫。那有没有好的整理方法呢？

如[Things You Didn't Know About Virtuoso: Customizing the Library Manager](https://community.cadence.com/cadence_blogs_8/b/cic/posts/things-you-didn-t-know-about-virtuoso-library-manager)一文中介绍的，Cadence在IC6.1之后提供了自定义的功能，主要分为**设置显示属性**和**创建合并Library**两种。

## 设置显示属性（set display attributes）

这个功能的用途是给指定的library设置颜色和图标。

具体的操作是：

1. 点击Library Manager的`Edit`-`Display Settings`，在弹出的窗口中选择`add`，再在弹出的窗口里输入一个有含义的名字，点击确定后可以看到这个名字出现在了左侧列表中；

2. 选中新加的名字，在右侧可以勾选`Using color`、`Using icon`，设置颜色和图标，同时可以在右下侧看到预览效果；

3. 点击save后前面所作的修改便会以xml的格式保存到Virtuoso启动目录的`.cadence/libmanager/xxx`文件中；

4. 修改`cds.lib`，在目标lib的define语句后面添加`ASSIGN libname DISPLAY display_name`，例如

   ```
   DEFINE my_lib ./my_lib
   ASSIGN my_lib DISPLAY blue
   ```

这个时候刷新Library Manager，就可以看到`my_lib`变成了蓝色字体，选中时会出现蓝色背景的样式。

## 创建合并Library（create combined libraries）

这个功能是通过创建一个*假lib（dummy lib）*，然后把指定的lib作为这个假lib的二级lib，来实现分组管理的目的。

具体的操作是：

1. 修改`cds.lib`，定义假lib；

2. 在假lib的定义语句后添加`ASSIGN libname COMBINE sub_lib1 sub_lib2`，例如

   ```
   DEFINE sub_lib1 ./sub_lib1
   DEFINE sub_lib2 ./sub_lib2
   DEFINE my_libs ./my_libs
   ASSIGN my_libs COMBINE sub_lib1 sub_lib2
   ```

这个时候刷新Library Manager，就可以看到`my_libs`前面多了个加号（+），点击后会显示二级lib。

PS，这个功能是可以依法创建三级lib或更多。

## 与版本管理工具的配合

通过设置显示属性的功能，可以很方便的把各lib的权限（只读、可读写）和状态（全部check-in、有check-out的、不是最新等）标注在Library Manager中，工作中一目了然。

> 因为家里没有Cadence的环境，所以没有提供截图，更多的可以参考[让你的Cadence Library更加美观](https://zhuanlan.zhihu.com/p/20739660)。