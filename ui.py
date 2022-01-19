import pygame.camera
import pygame.image
import numpy as np
import math
import ctypes
from threading import Thread
import yolo

ctypes.windll.user32.SetProcessDPIAware()


screen_w = 1280
screen_h = 720

#screen_w = 1920
#screen_h = 1080

center_x = screen_w*0.53
center_y = screen_h*0.5




cross_size = 20
cross_thickness = 3
circle_r = 15
circle_thickness = 2


    
    
class handler_class:
    def __init__(self):
        self.mouse_capturing = False
        self.ai_enabled = False
        
        self.circle_x = 0
        self.circle_y = 0
        
        self.motor = 0
        self.firing = False
        
        
        self.rad_per_pix = math.atan(math.sin(math.radians(43/2))/(screen_h/2)/math.cos(math.radians(43/2)))
        self.pix_per_rad = 1/self.rad_per_pix
        
        
        self.x_max_rad = self.rad_per_pix*screen_w/2
        self.y_max_rad = self.rad_per_pix*screen_h/2
        
        
        
        Thread(target=self.t1).start()
        #self.t1()
        
        
    def get_camera_view(self):
        return np.rot90(self.camera_view,3)[:, ::-1, :]
    
    def t1(self):
        
        pygame.init()
        pygame.camera.init()
        

        cameras = pygame.camera.list_cameras()

        print("Using camera %s ..." % cameras[0])

        webcam = pygame.camera.Camera(cameras[0],(screen_w,screen_h))

        webcam.start()

        screen = pygame.display.set_mode( ( screen_w, screen_h ) )

        myfont = pygame.font.SysFont('Segoe UI', 30)


        pygame.display.set_caption("pyGame Camera View")
        pygame.mouse.set_pos(center_x,center_y)
        
        
        
        img = webcam.get_image()
        
        pixArray = pygame.surfarray.pixels3d(img)
        self.camera_view = np.copy(pixArray)
        del pixArray
        
        
        ####################################################################################
        
        self.yolo_handler = yolo.handler(self.get_camera_view,[0],0.1,1)
        
        ####################################################################################
        
        while True :
            
            target_list = self.yolo_handler.l
            
            
            
            
            for e in pygame.event.get() :
                if e.type == pygame.QUIT :
                    pygame.quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_e:
                        self.circle_x = 0.0
                        self.circle_y = 0.0
                        self.mouse_capturing = not self.mouse_capturing
                        pygame.mouse.set_visible(not self.mouse_capturing)
                        pygame.event.set_grab(self.mouse_capturing)
                        
                    if e.key == pygame.K_y:
                        self.ai_enabled = not self.ai_enabled
                        self.yolo_handler.running = self.ai_enabled

                        
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        
                    if e.key == pygame.K_z:
                        self.motor = 1
                    if e.key == pygame.K_x:
                        self.motor = -1
                        
                        
                if e.type == pygame.MOUSEMOTION:
                    if self.mouse_capturing and not self.ai_enabled:
                        mx, my = e.rel
                        self.circle_x = np.clip(self.circle_x+mx*self.rad_per_pix,-self.x_max_rad,self.x_max_rad)
                        self.circle_y = np.clip(self.circle_y+my*self.rad_per_pix,-self.y_max_rad,self.y_max_rad)
                    
                            
                
                
                
            #print(self.circle_x,self.circle_y)

                    
            
            
            
            img = webcam.get_image()
            
            
            pixArray = pygame.surfarray.pixels3d(img)
            self.camera_view = np.copy(pixArray)
            del pixArray


            # draw frame
            screen.blit(img, (0,0))
            
            
            
            
            if self.ai_enabled:
                for i in target_list:
                    c1, c2, c3 = i
                    pygame.draw.rect(screen,'green', pygame.Rect(c1[0], c1[1], c2[0]-c1[0], c2[1]-c1[1]),  4)
                    pygame.draw.circle(screen,'green', (c3[0],c3[1]), 5, 5)

            
            
            
            if self.ai_enabled:
                self.firing = False
                if self.mouse_capturing:
                    for i in target_list:
                        c1, c2, c3 = i
                        if center_x ==  np.clip(center_x,c1[0],c2[0]) and center_y == np.clip(center_y,c1[1],c2[1]):
                            self.firing = True
                            pygame.draw.rect(screen,'red', pygame.Rect(c1[0], c1[1], c2[0]-c1[0], c2[1]-c1[1]),  4)
                    
            else:    
                self.firing = pygame.mouse.get_pressed()[0]
                #print(self.firing)
            

            if self.mouse_capturing and self.ai_enabled:
                nearest_tar_dist = None
                
                for i in target_list:
                    c1, c2, c3 = i
                    dist = np.hypot(c3[0]-center_x,c3[1]-center_y)
                    if nearest_tar_dist == None or nearest_tar_dist > dist:
                        nearest_tar_dist = dist
                        self.circle_x = (c3[0] - center_x)*self.rad_per_pix
                        self.circle_y = (c3[1] - center_y)*self.rad_per_pix
                        
            
            
            pygame.draw.line(screen, 'green', (center_x, center_y-cross_size), (center_x, center_y+cross_size),cross_thickness)
            pygame.draw.line(screen, 'green', (center_x-cross_size, center_y), (center_x+cross_size, center_y),cross_thickness)
            pygame.draw.circle(screen, 'green', (center_x+self.circle_x*self.pix_per_rad, center_y+self.circle_y*self.pix_per_rad), circle_r, circle_thickness)
            
            
            textsurface = myfont.render(f"Ai enabled: {self.ai_enabled}", False, (0, 255, 0))
            screen.blit(textsurface,(0,0))
            textsurface = myfont.render(f"Tracking enabled: {self.mouse_capturing}", False, (0, 255, 0))
            screen.blit(textsurface,(0,30))
            
            pygame.display.flip()
            # grab next frame    
    





handler = handler_class()

    