#!/usr/bin/env python
#coding:utf-8

import socket
import time
flag = True
host = '172.16.162.87'  #本机（主机）ip

port = 1026   # 自定义端口
def socket_server(flag):
    server = socket.socket()  # 默认AF_INET、SOCK_STREAM
    server.bind((host, port))  # 连接主机
    server.listen(5)  # 连接最多5个设备
    print('a')
    while True:
        connect, address = server.accept()  # 开始接收客户端连接请求
        print('b')
        # 处理连接交互信息
        while True:
            data = connect.recv(1024)  # 接收客户端发送的信息
            data = data.decode()
            if not len(data):
                print('链接已断开')
                break
            else:
                print('收到信息:%s' % data)

            # 信息回复
            g = "ok"
            g = g.encode()
            connect.send(g)

    server.close()


socket_server(flag)
