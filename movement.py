import time
import numpy as np
import serial
from threading import Thread


ser=serial.Serial(baudrate='115200', timeout=.5, port='/dev/ttyUSB0')	# choose your usb device



x_dir = -1    	# set value as 1 or -1
y_dir = -1    	# set value as 1 or -1

x_offset = 0    # used to tune center position
y_offset = 8	# used to tune center position

tar_x = 0
tar_y = 0

now_x = 0
now_y = 0


step_size = 1
sleep_time = 1/50



def deg2ms(deg,offset,dir):
    return np.int(np.clip((deg*dir+45+offset)/90*1000,1,999))
    
def ms2deg(ms,offset,dir):
    return ((ms/1000*90)-45-offset)*dir


def t1():
    global now_x
    global now_y
    while True:
        tmp_x = np.clip(tar_x, now_x-step_size, now_x+step_size)
        tmp_y = np.clip(tar_y, now_y-step_size, now_y+step_size)
        

        tmp_y = np.clip(tmp_y,-20,40)

        xms = deg2ms(tmp_x,x_offset,x_dir)
        yms = deg2ms(tmp_y,y_offset,y_dir)
        
        now_x = ms2deg(xms,x_offset,x_dir)
        now_y = ms2deg(yms,y_offset,y_dir)
        
        
        s = str(xms).zfill(3)+str(yms).zfill(3)
        #print(s)
        ser.write(bytes(s, 'ascii'))

        
        
        time.sleep(sleep_time)
        
        
Thread(target=t1).start()
        
        
        
        
        
        
        
        
        
        
        
        
