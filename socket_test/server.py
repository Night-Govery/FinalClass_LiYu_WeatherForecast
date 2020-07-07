#服务器
#服务器接收发送过来的min.json文件
#并将收到的json文件改写到receive.json文件里

#先运行server.py
#再运行client.py

import socket
import struct
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8000
server.bind(("127.0.0.1",port))
server.listen(5)

#打印出目前监听的端口
print('[+] Listen on %d' % port)
sock,addr = server.accept()
d = sock.recv(struct.calcsize("l"))
total_size = struct.unpack("l",d)
num  = total_size[0]//1024
data = b''
for i in range(num):
    data += sock.recv(1024)
data += sock.recv(total_size[0]%1024)

#将接收到的json文件改写进reeceive.json文件
with open("receive.json","wb") as f:
    f.write(data)
sock.close()
