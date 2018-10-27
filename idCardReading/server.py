import os
import socket
import struct
ip = (socket.gethostbyname(socket.gethostname()))
print(ip)
address = (ip, 4000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(1) 


client, addr = s.accept()

print('got connected from {}'.format(addr))

buf = bytes('','utf-8')
while len(buf)<4:
    buf += client.recv(4-len(buf))
size = struct.unpack('!i', buf)
print("receiving {} bytes".format(size))

with open(os.getcwd() + '/images/passportFromPhone.jpg', 'wb') as img:
    while True:
        data = client.recv(1024)
        if not data:
            break
        img.write(data)
print('received, yay!')


client.close()

