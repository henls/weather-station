# coding=UTF-8
import sys
sys.path.append(r'/home/pi/.local/lib/python3.7/site-packages')

from retrying import retry
import cv2
import time
@retry
def get_img_from_camera_net(folder_path):
    while 1:
        try:
            cap = cv2.VideoCapture(r"rtsp://admin:admin123@192.168.100.211:554/h264/ch1/main")#获取网络摄像机
            ret, frame = cap.read()
            #cv2.imshow("capture", frame)
            #print (str(i))
            cv2.imwrite(folder_path  + '.jpg', frame)# 存储为图像
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #   break
            #time.sleep(2)
            cv2.destroyAllWindows()
            cap.release()
            time.sleep(10)
 	except Exception as e:
            print(e)
            raise IOError('444')
# 测试
if __name__ == '__main__':
    folder_path = '/home/pi/Desktop/fuxianhu/task/www/metestat/heaven'
    get_img_from_camera_net(folder_path)
