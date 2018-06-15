# -*- coding: utf-8 -*-
import cv2
import math
import numpy as np


class IFrame:
    
    def __init__(self,im):
        self.im=im
        self.clicks=list()
        self.bac=[[0,0],[0,0]]
        
    def mouse_callback(self,event, x, y, flags, params):
        if event == 1:
            self.clicks.append([x, y])
    
    def set_bac(self,diaghg,diabd):
        self.bac[0]=diaghg
        self.bac[1]=diabd


    def getUserClicks(self,message):
        scale_width = 640 / self.im.shape[1]
        scale_height = 480 / self.im.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(self.im.shape[1] * scale)
        window_height = int(self.im.shape[0] * scale)
        cv2.namedWindow(message, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(message, window_width, window_height)
        cv2.setMouseCallback(message, self.mouse_callback)
        cv2.imshow(message, self.im)
        cv2.waitKey(4500)
        cv2.destroyAllWindows()
        
        
    def cut(self): 
        if self.bac==[[0,0],[0,0]]:
            print("bac non initialisé impossible de couper")
        else:
            self.im = self.im[self.bac[0][1]:self.bac[1][1],self.bac[0][0]:self.bac[1][0]]
            
    def resize(self,scale):
        self.im = cv2.resize(self.im, (0,0), 0, scale, scale, cv2.INTER_AREA)
        
    def rotate(self,angle):
        Rot = cv2.getRotationMatrix2D((math.floor(self.im.shape[1]/2),math.floor(self.im.shape[0]/2)), angle, 1)
        return(cv2.warpAffine(self.im,Rot,(self.im.shape[1],self.im.shape[0])))
        
    def rotate90(self):
        return(np.rot90(self.im))