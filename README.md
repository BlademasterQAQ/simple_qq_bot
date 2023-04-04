# 基于 [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的简易监听回复机器人

python代码部分参考：[使用go-cqhttp搭建QQ机器人_饭a的博客-CSDN博客](https://blog.csdn.net/qq_64126275/article/details/128586651)

## 使用方法

1. `git clone`或者下载解压本仓库源码
2. 修改`QQ_bot_listener.py`，在`设置区`填写需要命中的Q群群号和Q号，本demo会命中来自设定的群号和Q号的“@全体成员”消息。然后在`reply_message`中填写命中后回复信息的字符串（建议用`""`str类型）
   最后运行`QQ_bot_listener.py`（python缺少依赖请自行pip安装）
3. 修改`go-cqhttp_windows_amd64\config.yml`配置文件，在`uin: `和`password: `填入你的Q号和密码（密码填在单引号内）。
   双击`go-cqhttp_windows_amd64\go-cqhttp.bat`运行。

## 原理

​		 [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 本质上是一个QQ客户端，只是腾讯官方的客户端不同的是，**其为程序提供API接口，可以用程序自动读取QQ客户端的信息并回复**。

​		[Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 提供4种API工作方式，分为两种协议：http协议和websocket协议。其中http协议相对简单，网上的教程也多，推荐。

​		要实现QQ机器人，首先，我们需要**获取客户端接收的信息**，然后分析处理。http协议的获取信息方式采用**反向 HTTP POST**，即`go-cqhttp`在收到信息后，会用HTTP POST向指定的端口转发这个信息（默认**5701端口**）。**我们只需要在该端口用python程序开启http server，监听发送到该端口的数据，即可实现获取客户端接收的信息。**
​		在接受到信息后，我们可以对信息进行分析，然后回复特定的信息。在回复的时候，采用**正向HTTP API**，用指定的格式向`go-cqhttp`监听的5700端口发送HTTP GET即可。
