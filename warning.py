import sys
sys.path.append(r'/home/pi/.local/lib/python3.7/site-packages')
from buzzer import buzzer
import datetime
import time
def warning(filename):
    ring = 0
    fs = open(r'/home/pi/Desktop/fuxianhu/task/router/x_ray_event.txt','r')
    last = fs.read()
    fs.close()
    while 1:
        #print(ring)
        try:
            time.sleep(10)
            fs = open(filename,'r+')
            cont = fs.read()
            fs.close()
            cont = cont.split(',')
            fs = open(r'/home/pi/Desktop/fuxianhu/task/router/x_ray_event.txt','r')
            xray = fs.read()
            fs.close()
            if xray!=last:
                last = xray
                for i in range(200):
                    buzzer.warning()
                    time.sleep(0.1)
                buzzer.close()
            #if float(cont[2])>12 or float(cont[-2])>85 or float(cont[4])<=float(cont[-1]):
            if float(cont[2])>=12 and datetime.datetime.now().strftime('%H')<'19':
                for i in range(5):
                    buzzer.warning()
                    time.sleep(0.5)
                ring+=1
            else:
                ring = 0
                buzzer.close()
            if ring>=3:
                buzzer.warning_urgency()
        except Exception as e:
            print(e)
            print('***********')
           # print(cont)
            print('***********')

filename = r'/home/pi/Desktop/communication/latest.csv'
warning(filename)
