import numpy as np
import socket
import time
host='localhost'
port=4041
s=socket.socket()
s.bind((host,port))
s.listen(5)
data=[]
while 1:
    data1=np.random.uniform(-100,100,6)
    local_date=time.strftime("%F")
    local_time=time.strftime("%H:%M:%S")
    data.append(local_date)
    data.append(local_time)
    for i in range(len(data1)):
        data.append(data1[i])
    time.sleep(5)
    c,addr = s.accept()
    c.send(str(data).encode())
    data=[]
    c.close()

