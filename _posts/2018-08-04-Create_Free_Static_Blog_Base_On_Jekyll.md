---
layout:     post
title:      "基于Jekyll创建免费的静态博客站点"
date:       2018-08-04 01:26
author:     "MaZhaoxin"
header-img: "img/bg-post/coding.jpg"
catalog:    true
tags:
    - Programing
---

> 这篇算是交作业了。

## 写在前面的话

无意中在[知乎](https://www.zhihu.com/question/21172379/answer/62294047)看到了一个关于支持Markdown的博客平台的回答，结识了Jekyll。正好想更换博客平台，就查了些资料。

在建站时参考了[Jekyll搭建个人博客](http://baixin.io/2016/10/jekyll_tutorials1/)和[如何搭建个人网站](http://goileo.top/%E5%A6%82%E4%BD%95%E5%85%8D%E8%B4%B9%E4%B8%94%E5%BF%AB%E9%80%9F%E7%9A%84%E6%90%AD%E5%BB%BA%E4%B8%AA%E4%BA%BA%E7%BD%91%E7%AB%99)，又无意中看到了刚创建就被遗弃了的<http://zhaoxin.github.io/>。让我惊讶的是像下面所示的这样寥寥几个文件，居然就可以在浏览时显示出首页、目录、关于和文章这样完整的内容，并且如果想添加文章也只需要在`_posts`目录下放置Markdown文档即可。

```
│  about.md
│  index.md
│  _config.yml
│
└─_posts
        2017-02-04-welcome-to-jekyll.markdown
```

这种简约的结构和操作的便捷让我感到震惊，甚至还困惑了些许时间来思考它的运行原理。后来才明白是因为GitHub Pages原生支持Jekyll，所以并不需要像前面两篇文档所讲的那样要花费力气搭建本地服务器。

## Jekyll

Jekyll是基于Ruby的*静态网站生成器*，在很多介绍文档中都是从安装Ruby开始的，**但是这是没有必要的**。

Jekyll有两种用法：

- 其一是运行在本地，在本地存放Markdown文档，通过运行`build`命令生成纯静态站点后，把生成出来的文件上传到服务器，实现网站的功能；
- 其二则是让Jekyll运行在服务器上，所有相关文档都存放在服务器，不需要手动执行`build`命令，也不需要上传生成的东西，Jekyll会在有人浏览时自动解析出页面。

显然对于后者，本地是不需要装Ruby和Jekyll的。

## GitHub和Coding

GitHub和Coding都有支持Jekyll的Pages服务，它们在站点中起到了托管代码以及运行Jekyll的功能。

前者是大名鼎鼎的国际大站，但国内*局域网*访问速度不佳；后者是国内厂商，据说背后有腾讯撑腰，目前看使用便捷程度和访问速度都不错。

我选择了后者，还有一个考量是喜欢`coding.me`的域名。

Coding的注册和Pages服务的开通都很简单，具体的可以参见[创建静态 Coding Pages – CODING 帮助中心](https://coding.net/help/doc/pages/creating-pages.html)。

## Git

Git只是一个版本管理工具，类似SVN、SOS之类的，它所起到的作用是下载别人开源的项目、上传和管理自己的项目。

对于*创建静态博客站点*这一需求来说，只装Git就足够了。当然GitHub和Coding也支持在线创建文本文件（但不能创建文件夹，或者是我没找到），但是不够方便。常用的指令有：

```
git clone https://github.com/xxxx/yyyy			# 下载服务器上的项目到本地
git add *						# 标记待添加的文件
git rm xxxx						# 标记待删除的文件
git commit -m "blablabla"				# 执行标记的修改
git push						# 将本地数据同步到服务器
```

## 站在巨人的肩膀上

如果只想建立一个*看得过去的*博客站点，而专注于创造内容上，则完全没有必要从零开始。在建立站点时可以先`clone`一个页面设计符合自己审美的项目，然后在其之上修改。

我参考了知乎上的这个[问答](https://www.zhihu.com/question/20223939)，并选择了[黄玄](http://huangxuan.me/)的方案。

将他的项目`clone`到本地后所看到的目录结构是这样子的（移除了与Jekyll无关的内容）：

```
│  .gitignore					# 告诉Git哪些文件是不需要同步到服务器的
│  404.html					# 出现404错误时展示的页面
│  about.html					# About页面
│  feed.xml					# RSS订阅页面
│  index.html					# 默认展示页面（首页）
│  offline.html					# 网络中断时展示的页面
│  README.md					# 项目介绍
│  sw.js					# 提供预加载功能的脚本
│  tags.html					# 标签分类页面
│  _config.yml					# 站点配置文件
│  
├─css
│      .DS_Store
│      bootstrap.css
│      ...
│      
├─fonts
│      glyphicons-halflings-regular.eot
│      ...
│      
├─img
│  │  home-bg.jpg
│  │  avatar-hux.jpg
│  │  ...
│  │  
│  └─in-post
│      │  post-c-u-ali-079717.png
│      │  ...
│      │  
│      ├─post-alitrip-pd
│      │      post-alitrip-pd.013.jpg
│      │      ...
│      │      
│      └─...
│              
├─js
│      animatescroll.min.js
│      bootstrap.js
│      ...
│      
├─less
│      .DS_Store
│      hux-blog.less
│      mixins.less
│      ...
│          
├─_includes
│  │  footer.html
│  │  head.html
│  │  nav.html
│  │  
│  └─about
│          en.md
│          zh.md
│              
├─_layouts
│      default.html
│      page.html
│      post.html
│      
└─_posts
        2014-01-29-hello-2015.markdown
        2014-08-16-miui6.markdown
        ...
```

不难看出，除了css/less/font/js/img之类的网站必备目录外，还有几个以下划线开头的目录，它们都是Jekyll默认的功能目录：

```
_includes: 调用include时搜索的目录
_layouts: 页面布局
_posts: 博客文章存放目录，其中的文件必须是 YYYY-MM-DD-xxxxxxxx.md 格式的文件名
```

而根目录下的文件中最重要的是`_config.yml`，它提供了整个站点的参数配置。

在浏览首页时，大致的解析路线是

```
0. 载入站点信息：读取配置文件、遍历_posts下的内容等；
1. 解析index.html；
2. 根据index.html中指向的模板，解析_layouts/page.html；
3. 根据page.html中的include指令插入_includes/head.html等；
4. 在解析过程中根据Liquid模板语言自动插入站点信息；
5. 根据解析的HTML文档，由浏览器请求静态资源（css、js、img等）
```

关于图片文件的整理，我采取的方法略有不同。首先，我把题图放在了`./img/bg-post`下面，具体的图片文件名不再加bg等前缀；然后，我把文章插图放在了`./img/in-post/-YYYY-MM-DD-xxxxxxxx/`下面，具体的文件名也不再加其他前缀。文件插图目录前面之所以有一个`-`是因为这样在文章中引用时可以直接采用`![](/img/in-post/\{\{page.id | replace:'/','-'\}\}/xxx.png)`的统一语句。

## 总结

在搭建这个站点的过程中，我只安装了Git这一个软件，申请了Coding.net的一个帐号，除此之外无需任何其他的工具。

至此Powered by [Jekyll](https://jekyllrb.com/) 、Themed by [Hux](http://huangxuan.me) 、Hosted by [Coding Pages](https://pages.coding.me) 的博客站点建立完毕，万事俱备矣！