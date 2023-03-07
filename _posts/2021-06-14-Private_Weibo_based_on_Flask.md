---
layout:     post
title:      "基于Flask搭建私人微博"
date:       2021-06-14 17:31:51
author:     "MaZhaoxin"
header-img: "img/bg-post/coding.jpg"
catalog:    true
tags:
    - Programing
    - Flask
typora-root-url:	..
---

自从宝宝出生以来，就有了很多很多拍照、录视频的冲动，并且希望按照时间顺序整理记录下来。但手机相册起不到精选的效果，发微博、朋友圈又太过招人烦，即使设为自己可见也有把隐私交到别人手里、备份迁移不方便之类的顾虑（有人人网和网易博客的前例）。家里的群晖NAS闲着也是闲着，我就有了在上面搭个*简单的*网站，用来发一些文字、图片、视频的想法。

终于在今年春节假期时，利用3个睡午觉的时间，用Flask+Bootstrap做了第一阶段的实现。至今运行了4个月，感觉还不错，简陋是简陋了些，但又不是不能用……

![1623665014576](/img/in-post/2021-06-14-Private_Weibo_based_on_Flask.assets/1623665014576.png)

# 规划

## 功能

因为我能力有限，功能一定越简单越好，考虑只实现以下功能：

- 列表展示：类似微博或者朋友圈的样子，上面是文字，下面是图片九宫格；
- 详细展示：可以点进去看到大一些的图片，类似图片点开放大的效果；
- 发表界面：即用来发表新的微博，考虑到有可能会补发，因此提供一个手填时间的功能；
- 搜索：可以用关键字搜索文本内容；

其他的诸如评论、转发、点赞之类的交互功能全都不做，甚至为了留住真实的想法（主要是懒）连编辑功能都不做。

网站部署在NAS上，只提供内部局域网访问，以避免泄露隐私。

## 技术选型

上大学时我只学过ASP，不过现在对VB6这种老旧的编程语言实在是提不起兴趣来。基于“少写代码多做事”的基本思想考虑使用Python，而基于Python的Web框架中Flask比较轻，资料又全，因此后端就选择了Flask。

前端则选用了同样比较轻的Bootstrap，由于它是响应式布局，在电脑和手机上都有很好的效果。

至于数据库——我计划将上传的图片、视频以日期为目录存储在文件系统中，数据库里只存放文本，并且完全没有并发的需求，就用Python自带驱动的sqlite+数据库文件实现。

理论上还需要网关接口（WSGI），但同样因为没有并发需求，直接用Flask自带的开发服务器就得了。

# 具体实现

按照Flask的教程，至少要做3件事情：

- 编写数据模型（Model）：即数据要怎么存，每篇文章包含哪些要素；
- 编写视图函数（View）：其中包括了路由，即网址要怎么解析到各个功能上；
- 设计渲染模板（Template）：即打开网址后看到的页面长什么样。

下面按照各功能做个简单的介绍。

## 列表展示

首先考虑每篇文章的要素，应该包括索引号、文字、作者、附件路径（附件存储到文件系统中）、创建时间、记录时间。这里的记录时间即这件事发生的时间，是可以手填的。

``` python
class Post(db.Model):    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(100), nullable=False)
    attachments = db.Column(db.String(400), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now()) # new post created time
    record_time = db.Column(db.DateTime, nullable=False) # diary record time
```

展示的时候按照记录时间降序排列，每10篇分一页，格式是上面文字，中间图片，作者和日期放在下面的左右两侧，点击日期后进入详细展示页面，大约是下面的这种感觉。

![1623665803248](/img/in-post/2021-06-14-Private_Weibo_based_on_Flask.assets/1623665803248.png)

分页则采用Bootstrap自带的样式，清晰直接（*最讨厌瀑布流了，中间退出就不能接着看了*）。

![1623665906238](/img/in-post/2021-06-14-Private_Weibo_based_on_Flask.assets/1623665906238.png)

这里就不把模板代码放出来了，可以参考Flask+Bootstrap的相关教程和文档。

视图函数只需要下面简单的几行即可（真·少些代码多做事）。

``` python
@app.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.record_time.desc()).paginate(page, per_page=ITEMS_PER_PAGE)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, attach_type=attach_type)
```

## 详细展示

因为点击图片后左右滑动的效果我不会写，就用最简单的自上向下平铺的方式展示大图。

代码同样非常简单，这里多做了个异常处理，当根据索引号找不到文章时跳回首页并提示`No post found`。

``` python
@app.route('/view/<id>', methods=['GET'])
def view(id):
    post = Post.query.get(id)
    if post:
        return render_template('view.html', title='View', post=post, attach_type=attach_type)
    else:
        flash('No post found.', 'danger')
        return redirect(url_for('index'))
```

因为不支持流媒体播放，视频要下载下来才能观看。展示界面只放一个图片链接，点击后自动下载播放（幸好是在局域网内，有足够大的带宽，稍大的文件也只要略微一等就好）。

## 发表

发表界面自然要用到HTML表单（Form），这里采用Flask-WTF渲染。

``` python
class PostForm(FlaskForm):
    text = TextAreaField(render_kw={'placeholder': 'Enter anything you want to record ...'})
    author = StringField()
    attachments = MultipleFileField()
    record_time = StringField(description="When did it happen?", 
        render_kw={'placeholder': 'YYYY-MM-DD hh:mm:ss'})
    submit = SubmitField()
```

实际界面如下图所示：

![1623666563868](/img/in-post/2021-06-14-Private_Weibo_based_on_Flask.assets/1623666563868.png)

当点击`Submit`后，后端程序会把附件存到`/static/uploads/YYYY/MM/DD/`目录下（使用原文件名，其实这地方存在安全问题），并把路径记录到数据库中。如有多个附件，则用`|`符号分割。

## 搜索

搜索栏放置于banner位置，在电脑上看是在页面的右上角，在手机上看默认处于隐藏状态，点击菜单按钮后显示，效果如下图所示。

![1623671216529](/img/in-post/2021-06-14-Private_Weibo_based_on_Flask.assets/1623671216529.png)

后端程序获取到关键字后调用模型的`query.filter()`函数，以列表的形式展示，具体的代码也非常简单。

``` python
@app.route('/search', methods=['GET'])
def search():
    kw = request.args.get('kw', '', type=str)
    page = request.args.get('page', 1, type=int)
    
    pagination = Post.query.filter(Post.text.like('%'+kw+'%')).order_by(Post.record_time.desc()).paginate(page, per_page=ITEMS_PER_PAGE)
    posts = pagination.items
    return render_template('search.html', title='Search', kw=kw, posts=posts, pagination=pagination, attach_type=attach_type)
```

至此，这个网站的开发工作就基本结束了，数据模型的代码约15行，视图函数的代码约60行，渲染模板的代码总计约150行，再加上辅助函数等其他代码约20行，不得不说非常简约。

# 部署

群晖NAS默认是不支持部署Flask的，因此还有一点点工作要做。

以管理员身份登录NAS的Web管理界面后，在`套件中心`查找并安装Python3，在`控制面板 - 终端机和SNMP`中启动SSH功能。通过SSH连接到NAS后安装上传全部的文件，用`pip`命令安装所需要的包（见文尾总结），执行`run.py`后应该可以通过网址`http://NAS的IP:5000`看到页面（也可以用`.locals`域名访问，更简单方便）。`run.py`内容如下：

```python
from LifeDiary import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

为了防止有bug时Web自动退出，可以在`任务计划`中添加自动启动的指令，反正如果原先的没有退出，新的由于端口被占用也不会启动成功，不用担心有多个程序同时在跑的情况。

# 总结

虽然这个网站很简陋，但是我们用的还挺开心，至今4个月的时间发了约40篇*图文并茂*的生活琐事，也不枉我3天没睡午觉吧。XD

| 项目        | 内容                                         |
| ----------- | -------------------------------------------- |
| 后端语言    | Python                                       |
| 后端框架    | Flask                                        |
| 网关接口    | (无)                                         |
| 反向代理    | Nginx (NAS自带)                              |
| 前端框架    | Bootstrap                                    |
| 数据库      | sqlite+单文件                                |
| 后端插件/包 | flask-sqlalchemy, flask-wtf, bootstrap-flask |
| 前端插件/包 | (无)                                         |

> 最后，如果非得说ASP比Flask强的地方，我觉得是建立子站点。对于ASP来说，只要把文件复制过去，子站点就算建好了，因为它的路由系统就是文件系统。而Flask则需要注册，对我来说还是略嫌麻烦。
