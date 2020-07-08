'''
网页后端
    1.从网页前端获得日期数据date，并传入clienttt（）方法
    2.发送date到算法后端
    3.接收从算法后算传来的json文件并写入本地receive.json中
'''

import socket,struct,os
import json

class clienttt():
    def __init__(self,date):
        self.date = date.encode()    #要预测的日期

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1",8000))
        print('[+]connect successfully')
        #发送日期变量
        print(self.date)
        client.send(self.date)
        #接收json文件
        d = client.recv(struct.calcsize("l"))
        total_size = struct.unpack("l", d)
        num = total_size[0] // 1024
        data = b''
        for i in range(num):
            data += client.recv(1024)
        data += client.recv(total_size[0] % 1024)

        # 将接收到的json文件改写进receive.json文件
        with open("receive.json", "wb") as f:
            f.write(data)


        client.close()
