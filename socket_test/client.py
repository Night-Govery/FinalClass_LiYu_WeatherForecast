#客户端
#客户端发送文件到服务器
import socket,struct,os
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",8000))
print('[+]connect successfully')

#定义所发送的文件
#所发送的文件需在项目文件夹里
filepath = "min.json"
size =  os.stat(filepath).st_size
f= struct.pack("l",os.stat(filepath).st_size)
client.send(f)

img = open(filepath,"rb")
client.sendall(img.read())

img.close()
client.close()