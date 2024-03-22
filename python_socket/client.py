#!/usr/bin/env python
#coding:utf-8

import socket
import time

host = '192.168.137.11' #主机地址
#host = '172.16.162.87'  #本机（主机）ip
host = '192.168.137.11'
port = 1026

client = socket.socket()
client.connect((host, port)) #连接主机


s = input(">>")   #接收输入
s = s.encode()
client.send(s)   #发送给主机信息
data = client.recv(1024)  #接收主机回复信息

#主机回复信息处理
if data.decode()=='1':
        print('命令传输完成')
#print(data.decode())


