---
layout:     post
title:      "Flask App部署在子路径下的方法"
date:       2024-7-20 16:57
author:     "MaZhaoxin"
header-img: "img/bg-post/coding.jpg"
catalog:    true
tags:
    - Programing
    - Flask
typora-root-url:	..
---

> 之前提到，我基于Flask做了个简单的微博部署在了NAS上。如今已过了3年，当我想再加个应用时遇到了困难，因为域名只有一个，要怎么映射到多个站点上呢？如果站点的技术栈不同，有没有统一的部署方式？

## Nginx

Nginx的鼎鼎大名自然早有耳闻，但一直不知道有什么用。好像每次听到这个词，都会跟“负载均衡”、“反向代理”之类的词一起出现。就像有人说过的，“人们对名字的恐惧，超过了这个名字代表的事物”。

经过查询学习，了解到Nginx其实就相当于“银行网点的大堂经理”，当顾客（访问）到来时先看一下他要办什么业务，简单的业务（如图片之类的静态文件）就当场办理，复杂的业务（涉及到计算处理的）再根据业务类型分配到对应的柜台。

想一下我要实现什么效果：

1. 基于Flask的App不需要考虑自己会部署在哪个路径下，无论是根路径（`http://host/`）还是子路径（`http://host/app/`）都可以显示正确的画面、链接；
2. 当用户访问时，通过`http://host/app1/`可以访问App1，通过`http://host/app2/`可以访问App2，无论App1和App2是用什么语言、框架实现的。

Nginx这个大堂经理能起到分配业务作用的前提是，App1和App2已经开好了柜台，也就是它们有各自的访问端口，如：App1部署在`http://localhost:5001`上，App2部署在`http://localhost:5002`上。

接下来便是设置Nginx，制定分配规则。在安装完成后，有个自动生成的配置文件在`/etc/nginx/sites-available/default`，只需要在其中再添加一条规则即可。

``` nginx
location /app1/ {
        proxy_pass http://127.0.0.1:5001/app1/;
        proxy_redirect off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
}
```

这条规则的含义是把向`http://host/app1/*`的请求都转发到`http://127.0.0.1:5001/app1/*`，这是与具体的语言、框架无关的。*其中转发到的`/app1/`在我的需求中是必要的，在其他需求场景下可能不是，要具体情况具体分析。*

看起来，用子路径访问不同应用的需求已经解决了……吗？试一下发现并没有，App1提供的返回首页的链接会是`http://host/`而不是`http://host/app1/`，因为它不知道自己被部署到了子路径下面。

## WGSI

WGSI = Web Server Gateway Interface，它不是服务器，仅针对Python定义的一种接口规范（协议）。在这个协议框架下有服务器（Server）和应用（Application，App）两个组成部分：

- Server的实现有uWSGI、**Gunicorn**等；
- Application的实现有Django、**Flask**等。

在WGSI协议中有一个*意义不明*的`SCRIPT_NAME`参数，根据文档[Definitions of keys and classes — WSGI.org](https://wsgi.readthedocs.io/en/latest/definitions.html)中的说明，App可以通过这个参数**知道**自己的虚拟位置。它默认是个空字符串（`""`），代表了根路径（`/`）。

> **SCRIPT_NAME**
>
> The initial portion of the request URL’s “path” that corresponds to the application object, so that the application knows its virtual “location”. This may be an empty string, if the application corresponds to the “root” of the server.

那么显然，在部署时把这个参数设置为`"/app1"`就可以了。

> 分享个失败的经验，如果误把`SCRIPT_NAME`设置成`"/app1/"`（多了个反斜线），在访问`http://host/app1/`时会出现重定向的死循环。

## Gunicorn

Gunicorn可以用文件进行配置，这个配置文件是个Python脚本，其中标`important`的两行非常重要。

- 前者决定了柜台开在哪，要与大堂经理（Nginx）的认知（配置文件）一致；
- 后者则是子路径的设置。

``` python
# gunicorn.conf.py
workers = 1
threads = 2

bind = '127.0.0.1:5001'			# important
raw_env = ['SCRIPT_NAME=/app1']	# important

accesslog = '/var/log/gunicorn_access.log'
errorlog = '/var/log/gunicorn_error.log'
loglevel = 'warning'
```

启动Gunicon的命令为`/srv/web/bin/gunicorn -c ./gunicorn.conf.py run:app`，此时柜台便已开好。

## Flask

让我们回顾一下：

1. 用户访问`http://host/app1/`，Nginx会接收请求；
2. Nginx将请求转发给`http://127.0.0.1:5001/app1/`，Gunicorn会接收请求；
3. Gunicorn知道自己被部署在`/app1/`下面，于是把前缀`/app1`从请求中拿掉（如果直接访问`http://127.0.0.1:5001/`会因为无法去除前缀而报错），再发给Flask处理；

Flask照常解析、路由即可，但是页面中的链接要怎么保证是正确的呢？

显然，写死（hard-coding）的部分是无法正确处理的。而通过`url_for()`函数生成的链接，可以读取`SCRIPT_NAME`的设置，自动加上前缀，从而保证链接是正确的。也就是说，Flask App能正常运行还需要一个前提——**无论是js、css、image之类的静态文件，还是页面之间的链接，都要用`url_for()`生成。**

``` html
<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
<a class="navbar-brand" href="{{ url_for('index') }}">App Home</a>
```

> 此处还踩了一个坑：Flask配置参数中有个`APPLICATION_ROOT`看起来更“浓眉大眼”一些，实际上它也能为`url_for()`生成的链接添加前缀，但它并不能实现我想要的效果。*好像是它仅在请求外才能生效，用`with app.test_request_context()`测试是可以工作，在实际使用时却没生效，没有细究原因。*

## 总结

总结一下，其实Flask App还是会知道自己被部署到哪里，只是根据协议可以在不改动代码的方式，通过外部参数调整输出。Nginx作为直面用户的一环，根据链接模式（pattern）将请求转发到正确的端口。Gunicorn作为中间层负责处理请求地址并把参数告知Flask，Flask在用`url_for()`生成链接时再把前缀添加进去，完成闭环。

