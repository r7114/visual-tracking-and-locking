import numpy as np
from threading import Thread
import time
#from simple_pid import PID

class controller:
    def __init__(self, mh, ui):
        self.mh = mh
        self.ui = ui
        self.motor_speed = 7
        self.tracking_speed = 70
        
        self.smothing_a = 3
        self.smothing_b = 0.2
        self.smothing_c = 0.1
        self.smothing_d = 1
  
        Thread(target=self.t1).start()
    
    
    def get_speed(self,val):
        factor = (np.abs(val)-self.smothing_a)*self.smothing_b
        factor = np.clip(factor,self.smothing_c,self.smothing_d)
        return factor*self.tracking_speed
    
        
        
    def t1(self):
        
        #x_pid = PID(1, 0.1, 0.01, setpoint=0)
        #y_pid = PID(1, 0.1, 0.01, setpoint=0)

        while True:
            if self.ui.mouse_capturing:

                while True:
                    now_x = self.mh.x_pos
                    now_y = self.mh.y_pos
                    
                    
                    dx = np.rad2deg(self.ui.circle_x)/np.cos(np.deg2rad(now_y))
                    dy = np.rad2deg(self.ui.circle_y)
                    
                    
                    tar_x = now_x + dx
                    tar_y = now_y - dy
                    

                        
                     
                    
                    
                    
                    
                    
                    #tar_x = now_x - x_pid(np.rad2deg(self.ui.circle_x)/np.cos(np.deg2rad(now_y)))
                    #tar_y = now_y + y_pid(np.rad2deg(self.ui.circle_y))
                    
                    
                    xs = self.get_speed(dx)
                    ys = self.get_speed(dy)
                    
                    
                    self.mh.update_server_data(x=tar_x,y=tar_y,f=self.ui.firing,xs=xs,ys=ys)
                    #self.mh.update_server_data(x=tar_x,y=tar_y,f=self.ui.firing,xs=self.tracking_speed,ys=self.tracking_speed)
                    
                    if self.ui.motor == -1:
                        self.mh.update_server_data(m=0)
                        self.ui.motor = 0
                    if self.ui.motor == 1:
                        self.mh.update_server_data(m=self.motor_speed)
                        self.ui.motor = 0
                        
                    
                    time.sleep(0.05)
                    
                    old_x = now_x
                    old_y = now_y
                    now_x = self.mh.x_pos
                    now_y = self.mh.y_pos
                    
                    moved_x = now_x - old_x
                    moved_y = now_y - old_y
                    
                    
                    
                    self.ui.circle_x += -np.deg2rad(moved_x)
                    self.ui.circle_y += np.deg2rad(moved_y)
                    
                    
                    if not self.ui.mouse_capturing:
                        self.mh.update_server_data(m=0,f=False)
                        self.ui.motor = 0
                        break
                    
                time.sleep(0.1)


