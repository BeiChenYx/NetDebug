# NetDebug

#### 项目介绍


本项目使用pyqt5创建了一个网络调试助手,包含TCP/IP服务器，TCP/IP客户端，UDP/IP服务器， UDP/IP客户端

![整体效果](./main.png)

#### 软件架构

软件架构说明:

使用Python3的select库完成主要的socket的事件监听，进行异步操作socket;

#### 安装教程

克隆本项目

1. pip install pyqt5==5.10.1
2. python main.py