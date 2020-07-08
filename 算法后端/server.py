'''
算法后端
先运行算法后端（server.py）
算法后端  1.先接受网页后端传过来的日期变量并存进date变量
        2.将date作为参数传进ARIMA预测天气的方法并进行调用，生成json文件
        3.将json文件传到网页后端（client.py）
'''


import socket,os
import struct
from arima import Begin

class serverrr():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8000
    server.bind(("127.0.0.1",port))
    server.listen(5)

    #打印出目前监听的端口
    print('[+] Listen on %d' % port)
    sock,addr = server.accept()
    print('[+]connect successfully')
    #解码接收到的日期变量
    date = sock.recv(1024)
    date = date.decode()
    print(date)

    '''
    调用ARIMA方法，传入date参数并生成json文件准备传输
    '''
    b=Begin(date)
    b.begin()


    # 定义所发送的文件
    # 所发送的文件需在项目文件夹里
    filepath = "predict.json"
    size = os.stat(filepath).st_size
    f = struct.pack("l", os.stat(filepath).st_size)
    sock.send(f)

    img = open(filepath, "rb")
    sock.sendall(img.read())
    img.close()

    data = sock.recv(1024)
    print(data.decode())
    sock.close()