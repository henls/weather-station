import sys
sys.path.append(r'/home/pi/.local/lib/python3.7/site-packages')
from buzzer import buzzer
import time
import socket
from fso_mysqlpackage import mysql_fso
import matplotlib.pyplot as plt
from fso_communication import communication
import os
import pandas
import os
host='192.168.94.93'
port=1234
host1 = '192.168.94.93'
port1 = 8889
password1 = 'admin123'
user1 = 'root'
interval_time=10#setting the time between nearest two communication
#接受服务器数据
'''while 1:
    try:
        s = socket.socket()
        s.connect((host, port))
        data2=s.recv(1024).decode()[1:-1]
    except Exception as e:
        s = socket.socket()
        s.connect((host, port))
        data2=s.recv(1024).decode()[1:-1]
    else:
        break'''
'''while 1:
    try:
        data2 = communication.RecvData()
    except Exception as e:
        data2 = communication.RecvData()
    else:
        break'''
#print('开始通信')
nowtime = time.strftime("%H:%M:%S")
dateNow = time.strftime("%F")
if (int(nowtime.split(':')[1])>=59 and int(nowtime.split(':')[0])==23) or (int(nowtime.split(':')[0])>=0 and int(nowtime.split(':')[0])<6):
    data2 = [dateNow,nowtime,0,0,0,0,0,0,0,0]
    time.sleep(10)
else:
    data2 = communication.RecvData()
print('通信一次')
#print(data2)
#将数据写到本地文件data.csv
#data2=['2019-09-03','16:15:14',23,14,15,18,14,15,12,14]
#dateNow=time.strftime("%F")
dateYear=dateNow.split('-')[0]
try:
   # os.mkdir(r'/home/pi/Desktop/communication/'+dateYear)
    os.mkdir(r'/fso-weather-data/'+dateYear)
except Exception as e:
    pass
print('检查文件夹是否存在已完成')
#fs=open(r'/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv','a+')
fs = open(r'/fso-weather-data/'+dateYear+'/fso-weather-'+dateNow+'.csv','a+')
latest = open(r'/home/pi/Desktop/communication/latest.csv','w+')
latest.writelines(str(data2)[1:-1]+'\n')
latest.close()
if os.path.exists(r'/fso-cache/missing.csv'):
    missing = open(r'/fso-cache/missing.csv','a+')
    missing.writelines(str(data2)[1:-1]+'\n')
    missing.close()
#data2=str(data2)[1:-1]

fs.writelines(str(data2)[1:-1]+'\n')
fs.close()
filename=r'/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv'
#print(data2)
data2=str(data2)
data=data2[1:-1].split(',')
#print(data)
date=''
Time=''
speed=0
rain=0
temp=0
press=0
rad=0
dire=0
hum = 0
dew = 0
phy=[date, Time, speed, rain, temp, press, rad, dire, hum, dew]
save=['date', 'time', 'speed', 'rain', 'temp', 'press', 'rad', 'dire', 'hum', 'dew']
phy_plot=[]
ring=0
while 1:
    #dateNow=time.strftime("%F")
    for i in range(len(phy)):
        #绘制物理量的图形
        try:
            phy[i]=float(data[i])
        except Exception as e:
            continue
    #draw pictures
    #draw_name=r'/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv'
    draw_name = r'/fso-weather-data/'+dateYear+'/fso-weather-'+dateNow+'.csv'
    #***************************************************
    #print('开始画图')
    #communication.Fso_draw(draw_name)
    #超阈值预警
    #print('画图完成，开始判断预警')
    
    '''if phy[2]>12 or phy[-2]>85 or phy[4] <= phy[-1]:
        for i in range(5):
            buzzer.warning()
        ring+=1
    else:
        buzzer.close()
        ring=0
    if ring==3:
        buzzer.warning_urgency()'''
            #print('speed:{0}  hum:{1}  dew:{2}  temp{2}'.format(speed>12,hum>85,temp<=dew))
    #print(data[1][2:-1])
    #将数据写入数据库
            
    #print('sql insert')
    '''print(data[0][1:-1], data[1][2:-1], float(data[2]), float(data[3]),
                     float(data[4]), float(data[5]), float(data[6]), float(data[7]), float(data[8]), float(data[9]))'''
    #mysql_fso.insert(host1,user1,password1,data[0][1:-1],data[1][2:-1],float(data[2]),float(data[3]),float(data[4]),float(data[5]),float(data[6]),float(data[7]))
    '''mysql_fso.insert(host1, user1, password1, data[0][1:-1], data[1][2:-1], float(data[2]), float(data[3]),
                     float(data[4]), float(data[5]), float(data[6]), float(data[7]), float(data[8]), float(data[9]))'''
    #communication.fso_mysql(filename,host1,user1,password1)
    #print(data2)
    #communication.sql_remote(str(data2)[1:-1],host,port)
    #print('sql insert succed')
    #ans=fso_sqlite.find(host1,port1,'2019-08-18','DATA',cont='TEMP')
    #ans=fso_sqlite.find(host1,port1)
    #print(str(ans))

    '''s = socket.socket()
    s.connect((host, port))
    data2=s.recv(1024).decode()[1:-1]'''
    #time.sleep(interval_time)
    #获取气象数据
    '''while 1:
        try:
            data2 = communication.RecvData()
        except Exception as e:
            data2 = communication.RecvData()
        else:
            break'''
    nowtime = time.strftime("%H:%M:%S")
    dateNow = time.strftime("%F")
    if (int(nowtime.split(':')[1])==59 and int(nowtime.split(':')[0])==23) or (int(nowtime.split(':')[0])>=0 and int(nowtime.split(':')[0])<6):
        data2 = [dateNow,nowtime,0,0,0,0,0,0,0,0]
        time.sleep(10)
    else:
        data2 = communication.RecvData()
    #dateNow=time.strftime("%F")
    dateYear=dateNow.split('-')[0]
    try:
        #os.mkdir(r'/home/pi/Desktop/communication/'+dateYear)
        os.mkdir(r'/fso-weather-data/'+dateYear)
    except Exception as e:
        pass
    
    #fs=open(r'/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv','a+')
    fs = open(r'/fso-weather-data/'+dateYear+'/fso-weather-'+dateNow+'.csv','a+')
    fs.writelines(str(data2)[1:-1]+'\n')
    filename=r'/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv'
    fs.close()
    latest = open(r'/home/pi/Desktop/communication/latest.csv','w+')
    latest.writelines(str(data2)[1:-1]+'\n')
    latest.close()
    if os.path.exists(r'/fso-cache/missing.csv'):
        missing = open(r'/fso-cache/missing.csv','a+')
        missing.writelines(str(data2)[1:-1]+'\n')
        missing.close()
    data=str(data2)[1:-1].split(',')
    #print(data2)
    #print(data2[1:-1])
    #print(data)
