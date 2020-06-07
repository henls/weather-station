import socket
import os
import struct
import time
import datetime
import re
import sys
sys.path.append(r'/home/pi/.local/lib/python3.7/site-packages')
import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as ticker
from fso_mysqlpackage import mysql_fso
from retrying import retry
import matplotlib.animation as animation
#log = open('/home/pi/Desktop/write.log','a+')
#sys.stdout = log
#sys.stderr = log
def add_binary_nums(x, y):
    max_len = max(len(x), len(y))

    x = x.zfill(max_len)
    y = y.zfill(max_len)

    result = ''
    carry = 0

    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1

    if carry != 0: result = '1' + result

    return result.zfill(max_len)

@retry
def get_data(inf,host='192.168.100.125',port= 50000):
    s = socket.socket()  # 创建 socket 对象
    host = host  # 获取本地主机名
    port = port  # 设置端口号
    s.settimeout(3)
    '''气象站通信地址是x01，校验码CRC16：xa9/xc0（底前高后）'''
    #fs=open(r'/home/pi/Desktop/bug.txt','w+')
    #print(time.strftime('%F')+' '+time.strftime('%H:%M:%S')+'------'+'准备连接')
    s.connect((host, port))
    #print('连接成功')
    #fs.close()
    #s.settimeout(None)
    #print('connected')
    data=[]
    isTrue=True
    while isTrue or len(data)!=7:
        try:
            req = struct.pack('4B',0x00,0x50,0x01,0x8c)
            s.send(req)
            s.recv(1024)
            time.sleep(0.4)
            req = struct.pack(inf[0],inf[1],inf[2],inf[3],inf[4],inf[5],inf[6],inf[7],inf[8])
            #print('sending')
            s.send(req)
            #print('recving')
            #data=s.recv(1024)
            data = s.recv(7)
            crc=[]
            for q in data:
                #if len(str(q))==1:
                #    crc.append('0x'+'0'+str(hex(q)[2:]))
                #else:
                #    crc.append(str(hex(q)))
                if q<16:
                    crc.append('0x'+'0'+hex(q)[-1])
                else:
                    crc.append(hex(q))
            #print(data)
            #print(crc)
            # choose the true answer
            
            
            isTrue=bool(int(crc16(len(crc),crc),16))
            #print(isTrue)
            
            
            
            
            
            
            
            data=[]
            #data=str(data).split('\\')
            for ll in crc:
                data.append(ll[2:])
            
            #print(data)
            
            #print(data)
        #except BrokenPipeError:
        except Exception as e:
            
            #print(e)
            raise IOError("Broken Connected")
            s = socket.socket()  # 创建 socket 对象
            host = host  # 获取本地主机名



            port = port  # 设置端口号
            '''气象站通信地址是x01，校验码CRC16：xa9/xc0（底前高后）'''
            s.connect((host, port))
            #print('连接成功')
            req1 = struct.pack('4B', 0x00, 0x50, 0x01, 0x8C)#切换通信模式为Modbus
            s.send(req1)
            s.recv(1024)
            #req = struct.pack(inf)
            req = struct.pack(inf[0],inf[1],inf[2],inf[3],inf[4],inf[5],inf[6],inf[7],inf[8])
            #time.sleep(0.01)
            time.sleep(0.4)
            s.send(req)
            data=s.recv(7)
            crc=[]
            for q in data:
                crc.append(str(hex(q)))
            #print(data)
            #print(crc)
            # choose the true answer
            
            
            isTrue=bool(int(crc16(len(crc),crc),16))
            #print(isTrue)
            
            
            
            
            
            
            
            data=[]
            #data=str(data).split('\\')
            for ll in crc:
                data.append(ll[2:])
            #print(data)
            #print('异常捕获')
    return data

def RecvData():
    host='192.168.100.125'
    port= 50000
    local_date=time.strftime("%F")
    local_time = time.strftime("%H:%M:%S")
    res=[]#存放获取到的最新数据
    res.append(local_date)
    res.append(local_time)
    list = [['8B', 0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0A], ['8B', 0x01, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD5, 0xCA], ['8B', 0x01, 0x03, 0x00, 0x02, 0x00, 0x01, 0x25, 0xCA], ['8B', 0x01, 0x03, 0x00, 0x04, 0x00, 0x01, 0xC5, 0xCB], ['8B', 0x01, 0x03, 0x00, 0x05, 0x00, 0x01, 0x94, 0x0B], ['8B', 0x01, 0x03, 0x00, 0x06, 0x00, 0x01, 0x64, 0x0B], ['8B', 0x01, 0x03, 0x00, 0x08, 0x00, 0x01, 0x05, 0xC8]]
    para = ['风速', '雨量', '温度', '气压', '辐射', '风向','湿度','露点']
    speed=''
    run=''
    temp=''
    press=''
    rad=''
    dire=''
    hum = ''
    dew = ''
    phy=[speed,run, temp, press, rad, dire, hum, dew]
    #start=datetime.datetime.now()
    for i in range(len(list)):
        phy[i] = get_data(list[i],host,port)[3:5]
        #phy[i] = get_data(list[i])
        if para[i]=='湿度':#精度0.1，准确度+-5%
            #print('i:'+str(i))
            #print(para[i] + ':{}'.format(phy[i]))
            data = ''
            for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                data += ans
            phy[i] = int(data.replace(',',''), 16)/10
            #print(data)
            #phy[i] = round(int(data, 16)/1000,2)
            while phy[i]<1 or phy[i]>100:
                #print('humidty circle')
                phy[i] = get_data(list[i],host,port)[3:5]
                data = ''
                for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                    data += ans
                #match = re.findall('[0-9,a-f]{2}', str(phy[i]))
                #data = match[1]+match[0]
                phy[i] = int(data.replace(',',''), 16)/10
                #phy[i] = rpund(int(data, 16)/1000,2)
            #print(para[i] + ':{}'.format(phy[i]))
            #print(str(phy[i])+'%')
        elif para[i]=='风速':#精度0.1，范围0-45，准确度0.3+-0.003m/s
            #print(para[i]+':{}'.format(phy[i]))
            data=''
            #value=0
            #print(phy[i])
            for ans in re.findall('[0-9,a-f]{1,2}',str(phy[i])):
                #print(ans)
                data+=ans
                #value+=1
            #print(data)
            phy[i]=int(data.replace(',',''),16)/10
            #print(phy[i])
            while phy[i]<0 or phy[i]>=15:
                #print('speed circle')
                phy[i] = get_data(list[i],host,port)[4:6]
                data = ''
                value=0
                for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                    data += ans
                    value+=1
                phy[i] = int(data.replace(',',''), 16)/10
                #print(phy[i])
            #print(para[i] + ':{}'.format(phy[i]))
            #print(str(phy[i])+'m/s')
            #print('over')
        elif para[i]=='雨量':#精度0.2mm/min范围0-4mm，准确度+-3%
            #print(para[i] + ':{}'.format(phy[i]))
            data = ''
            for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                data += ans
            phy[i] = int(data.replace(',',''), 16)*0.2
            #print(para[i] + ':{}'.format(phy[i]))
            #print(str(phy[i])+'mm/min')
        elif para[i] == '温度':#精度0.1，范围-50-100 准确度+-0.5
            
            #print(para[i] + ':{}'.format(phy[i]))
            data = ''
            value=0
            for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                data += ans
               #value += 1
            
            #print(data)
            phy[i] = round(int(data.replace(',',''), 16)*0.1,2)
            if len(bin(int(phy[i]*10)))!=18:
                while phy[i]<0 or phy[i]>50:
                    #print('temperature circle')
                    phy[i] = get_data(list[i],host,port)[3:5]
                    data = ''
                    #value=0
                    for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                        data += ans
                        #value+=1
                    phy[i] = round(int(data.replace(',',''), 16)*0.1,2)
                #print(para[i] + ':{}'.format(phy[i]))
                #print(str(phy[i])+'℃')
            else:
                #print('temperature signed')
                sigphy=''
                if bin(int(phy[i]*10))[2]==1:
                    bits=bin(phy[i]*10)[2:]
                    for bit in bits:
                        if bit=='1':
                            sigphy+='0'
                        else:
                            sigphy+='1'
                    phy[i]=round(float('-'+str(int(sigphy,2)+1))/10,2)
                    #print(para[i] + ':{}'.format(phy[i]))
                    #print(str(phy[i])+'℃')
            #print('over')
        elif para[i] == '气压':#精度0.1，范围10-1100hpa，准确度+-0.3hpa
            #print(para[i] + ':{}'.format(phy[i]))
            data = ''
            for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                data += ans
            #print(data)
            phy[i] = round(int(data.replace(',',''), 16)*0.1,2)
            while phy[i]<0 or phy[i]>1100:
                #print('press circle')
                phy[i] = get_data(list[i],host,port)[3:5]
                data = ''
                for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                    data += ans
                phy[i] = round(int(data.replace(',',''), 16)*0.1,2)
            #print(para[i] + ':{}'.format(phy[i]))
            #print(str(phy[i])+'hpa')
            #print('气压：'+str(phy[i]))
        elif para[i] == '辐射':#精度1，范围0-2000w/m2，准确度+-5%
            #print(para[i] + ':{}'.format(phy[i]))
            data = ''
            #value=0
            for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                data += ans
                #value+=1
            phy[i] = int(data.replace(',',''), 16)
            #print(data)
            while phy[i]<0 or phy[i]>2000:
                #print('radiation circle')
                phy[i] = get_data(list[i],host,port)[3:5]
                data = ''
                value=0
                for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                    data += ans
                    value+=1
                phy[i] = int(data.replace(',',''), 16)
            #print(para[i] + ':{}'.format(phy[i]))
            #print(str(phy[i])+'W/㎡')
            #print('over')
        elif para[i] == '风向':#精度1，范围0-360，准确度+-3
            #print(para[i] + ':{}'.format(phy[i]))
            data = ''
            #value=0
            for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                data += ans
                #value+=1
            phy[i] = int(data.replace(',',''), 16)
            #print(data)
            while phy[i]<0 or phy[i]>360:
                #print('wind dir circle')
                phy[i] = get_data(list[i],host,port)[3:5]
                data = ''
                value=0
                for ans in re.findall('[0-9,a-f]{1,2}', str(phy[i])):
                    data += ans
                    value+=1
                phy[i] = int(data.replace(',',''), 16)
            #print(para[i] + ':{}'.format(phy[i]))
            #print(str(phy[i])+'°')
    #phy[-1] = round(phy[2]/phy[-2],2)
            #print('over')
    phy[-1] = round(phy[-2]*(0.198+0.0017*phy[2])+0.84*phy[2]-19.2,1)
    for i in range(len(phy)):
        res.append(phy[i])
    return res


font = FontProperties(fname="/home/pi/Desktop/GB2312.ttf",size=15)
ess=0
def Fso_draw(filename):
    dateNow=time.strftime("%F")
    try:
        fs = open(filename,'r+')
        fs.close()
    except Exception as e:
        fs = open(filename,'a+')
        fs.close()
    
    fs = open(filename,'r+')
    cont = fs.readlines()
    fs.close()
    ans = ''
    for i in cont:
        ans+=i
    
    ans=ans.replace(',',' ').replace('\n',' ')
    ans = ans.split(' ')
    num=[]
    for i in range(len(ans)):
        try:
            if len(ans[i])!=0:
                num.append(float(ans[i]))
            else:
                continue
        except Exception as e:
            num.append(ans[i])
            pass
    
    num = np.array(num)
    
    save = ['speed', 'rain', 'temp', 'press', 'rad', 'dire', 'hum', 'dew']
    saveCH=['风速','雨量','温度','气压','辐射强度','风向','相对湿度','露点温度']
    data = pandas.DataFrame(num.reshape(-1,10),columns=['date', 'time', 'speed', 'rain', 'temp', 'press', 'rad', 'dire', 'hum', 'dew'])
#print(RecvData())
#print('Time used:{}'.format(datetime.datetime.now()-start))
    str_draw=[['speed'],['rain'], ['temp'], ['press'], ['rad'], ['dire'], ['hum'], ['dew']]
    #**********************************************************************************************新加
    x = np.array(data.reindex(columns=['time']))
    ax = []
    plt.cla()
    plt.rcParams['figure.figsize'] = (21.0, 9.0)
    fig, axx = plt.subplots(nrows=1)
    plt.xticks(rotation=90)
    plt.xlabel('时间',fontproperties=font)
    plt.tick_params(labelsize=7)
    axx.xaxis.set_major_locator(ticker.MultipleLocator(3))
    for xx in x:
        ax.append(xx[0][1:-1])
    y = []
    img = np.array(data.reindex(columns=str_draw[7]))
    for ss in img:
        y.append(float(ss[0]))

    lines = [axx.plot(ax, y, linewidth=2.0)[0]]

    def animate(wid):
        lines[0].set_ydata(y)
        plt.ylim(wid)
        return lines
    #**************************************************************************************************
    ess=time.time()
    for i in range(len(str_draw)):
        y=[]
        img=np.array(data.reindex(columns=str_draw[i]))
        for ss in img:
            y.append(float(ss[0]))
        plt.ylabel(saveCH[i], fontproperties=font)
        ani = animation.FuncAnimation(fig, animate, [(min(y), max(y))], interval=0, blit=False)
        




        try:
            os.mkdir(r'/home/pi/Desktop/fuxianhu/task/www/metestat/'+dateNow)
        except Exception as e:
            pass
        plt.savefig(r'/home/pi/Desktop/fuxianhu/task/www/metestat/'+dateNow+'/'+save[i-1]+dateNow+'.jpg',format='jpg')
    plt.close('all')
    #print(time.time()-ess)
'''dateNow=time.strftime("%F")
dateYear=dateNow.split('-')[0]
draw_name=r'/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv'
Fso_draw(draw_name)'''


def fso_mysql(filename,host1,user1,password1):
    #print('sql insert')
    '''print(data[0][1:-1], data[1][2:-1], float(data[2]), float(data[3]),
                     float(data[4]), float(data[5]), float(data[6]), float(data[7]), float(data[8]), float(data[9]))'''
    #mysql_fso.insert(host1,user1,password1,data[0][1:-1],data[1][2:-1],float(data[2]),float(data[3]),float(data[4]),float(data[5]),float(data[6]),float(data[7]))
    fs=open(filename,'r+')
    host1=host1
    user1=user1
    password1=password1
    data=fs.readlines()
    data=data[len(data)-1][0:-1].split(',')
    #print(data)
    #print(float(data[3][1:]))
    #
    #
    mysql_fso.insert(host1, user1, password1,data[0][1:-1], data[1][2:-1], float(data[2][1:]), float(data[3][1:]),
                     float(data[4][1:]), float(data[5][1:]), float(data[6][1:]), float(data[7][1:]), float(data[8][1:]), float(data[9][1:]))
    #print('sql insert succed')

'''dateNow=time.strftime("%F")
dateYear=dateNow.split('-')[0]
filename=r'/home/pi/Desktop/communication/'+dateYear+'/data'+dateNow+'.csv'
host1 = '192.168.94.93'
user1 = 'root'
password1 = 'admin123'
fso_mysql(filename,host1,user1,password1)'''
@retry
def sql_remote(data,host,port):
    data = data
    host = host
    port = port
    try:
        #print('与虚拟服务器通信')
        s = socket.socket()
        s.settimeout(3)
        #print((host,port))
        s.connect((host, port))
        s.send(data.encode())
        s.close()
        #print('通信成功')
    except Exception as e:
        print(e)
        s.close()
        raise IOError("Broken Connected")
    
    
    


def crc16(datalen,p):
    CRC16Lo = 0xff
    CRC16Hi = 0xff
    CL = 0x01
    CH = 0xa0
    for i in range(datalen):
        CRC16Lo ^= int(p[i],16)
        #print(CRC16Lo)
        for FLAG in range(8):
            SaveHi = CRC16Hi
            SaveLo = CRC16Lo
            CRC16Hi >>= 1
            CRC16Lo >>= 1
            if(SaveHi & 0x01) == 0x01:
                CRC16Lo |= 0x80
            if(SaveLo & 0x01) == 0x01:
                CRC16Hi ^= CH
                CRC16Lo ^= CL
    return hex((CRC16Hi << 8) | CRC16Lo)
'''choose=['0x01', '0x03', '0x02', '0x01', '0x00', '0xb9', '0xd4']

ls=int(crc16(len(choose),choose),16)
print(ls)'''
