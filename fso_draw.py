import sys
sys.path.append(r'/home/pi/.local/lib/python3.7/site-packages')
import pandas
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as ticker
import os
import matplotlib.dates
import datetime
font = FontProperties(fname="/home/pi/Desktop/GB2312.ttf",size=15)

def Fso_draw(filename):
    dateNow = time.strftime("%F")
    try:
        fs = open(filename, 'r+')
        fs.close()
    except Exception as e:
        fs = open(filename, 'a+')
        fs.close()

    fs = open(filename, 'r+')
    cont = fs.readlines()
    fs.close()
    ans = ''
    for i in cont:
        ans += i

    ans = ans.replace(',', ' ').replace('\n', ' ')
    ans = ans.split(' ')
    num = []
    for i in range(len(ans)):
        try:
            if len(ans[i]) != 0:
                num.append(float(ans[i]))
            else:
                continue
        except Exception as e:
            num.append(ans[i])
            pass

    num = np.array(num)

    save = ['speed', 'rain', 'temp', 'press', 'rad', 'dire', 'hum', 'dew']
    saveCH = ['风速', '雨量', '温度', '气压', '辐射强度', '风向', '相对湿度', '露点温度']
    data = pandas.DataFrame(num.reshape(-1, 10),
                            columns=['date', 'time', 'speed', 'rain', 'temp', 'press', 'rad', 'dire', 'hum', 'dew'])
    # print(RecvData())
    # print('Time used:{}'.format(datetime.datetime.now()-start))
    str_draw = [['speed'], ['rain'], ['temp'], ['press'], ['rad'], ['dire'], ['hum'], ['dew']]
    x = np.array(data.reindex(columns=['time']))
    ax = []
    for xx in x[2:]:
        ax.append(xx[0][1:-1])
    draw_ax = []
    a = 100
    for xxx in ax:
        min = int(xxx.split(':')[1])
        if min%10==0 and min!=a:
            a = min
            draw_ax.append(xxx)
    draw_ax_tick = [datetime.datetime.strptime(t, '%H:%M:%S') for t in draw_ax]
    ax_tick = [datetime.datetime.strptime(t, '%H:%M:%S') for t in ax]
    for i in range(len(str_draw)):
        y = []
        img = np.array(data.reindex(columns=str_draw[i]))
        for ss in img[2:]:
            y.append(float(ss[0]))

        #        x = np.array(data.reindex(columns=['time']))
        #        ax=[]
        #        for xx in x:
        #            ax.append(xx[0][1:-1])
        plt.rcParams['figure.figsize'] = (21.0, 9.0)
        fig, axx = plt.subplots(1, 1)
        plt.cla()
        axx.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M:%S'))
        axx.axes.set_xticks(draw_ax_tick)
        axx.axes.set_xticklabels(draw_ax,rotation=40)
        #plt.xticks(rotation=90)
        # font = FontProperties(fname="/home/pi/Desktop/GB2312.ttf",size=15)
        # plt.margins(0)
        #axx.plot(ax, y, linewidth=2.0)
        #plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.text(ax_tick[np.array(y).argmax()],max(y),str(max(y)),fontdict={'color':'red'})
        plt.text(ax_tick[np.array(y).argmin()],np.array(y).min(),str(np.array(y).min()),fontdict={'color':'red'})
        
        indexof = np.where(np.array(ax)>'06:00:00')[0][0]
        #print(indexof)
        plt.text(ax_tick[0],max(y)+0.01,'均值:'+str(round(np.array(y)[indexof:].mean(),1)),fontproperties=font,fontdict={'color':'red'})
        # plt.rcParams['figure.dpi']=150
        plt.xlabel('时间', fontproperties=font)
        plt.ylabel(saveCH[i], fontproperties=font)
        plt.tick_params(labelsize=7)
        #axx.xaxis.set_major_locator(ticker.MultipleLocator(3))
        axx.plot(ax_tick, y, linewidth=2.0)
        try:
            os.mkdir(r'/home/pi/Desktop/fuxianhu/task/www/metestat/' + dateNow)
        except Exception as e:
            pass
        plt.savefig(r'/home/pi/Desktop/fuxianhu/task/www/metestat/' + dateNow + '/' + save[i] + dateNow + '.jpg',
                    format='jpg')
        plt.close('all')

if __name__=='__main__':
    dateNow = time.strftime("%F")
    dateYear = dateNow.split('-')[0]
    filename = r'/fso-weather-data/'+dateYear+'/fso-weather-'+dateNow+'.csv'
    Fso_draw(filename)
