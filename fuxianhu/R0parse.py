import re
import os
import time

def parse(url,save):
    url = url
    save = save
    r0 = 0
    while 1:
        time.sleep(10)
        value = os.popen('curl '+url)
        html = value.read()
        R0 = re.findall(r'[R0:]\d+[.]\d+',html)
        obsertime = re.findall(r'[RT = \']\d{6}',html)
        if len(R0) != 0:
            if r0 != R0[0][1:]:
                r0 = R0[0][1:]
                obser = obsertime[0][1:]
                f = open(save,'w')
                f.writelines(obser+'\t'+r0)
                f.close()


if __name__ == '__main__':
    url = '192.168.87.56:8889/LatestNvstImage/'
    save = r'/home/pi/Desktop/fuxianhu/r0.txt'
    parse(url,save)
