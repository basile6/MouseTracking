# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import math
import cv2
import numpy as np

import Thresholding.Binary


class Frame:
       
    def __init__(self,im,bary,bac,angle,seuil,horizontal):
        self.bary=bary
        self.bac=bac
        self.im=im
        if horizontal==False:
            self.im=self.rotate90()
        self.im = self.rotate(angle)
        self.im=self.cut(self.im)
        
#        self.showFrame(4)
        
        self.im = Thresholding.Binary.SeuillageBinaire(self.im,seuil)
                
    def mouseActualisation(self):
        if self.im[self.bary[1]][self.bary[0]]==0:
            print("lost mouse")
            self.bary=self.retrieveMouse()
        
        for i in range(10):
            self.actualiseBary()
        
                    
    def showFrame(self,l):
        largeur=self.im.shape[1]
        hauteur=self.im.shape[0]
        fig=plt.figure(figsize=(6,4))
        ax = fig.add_subplot(111)
        ax.imshow(self.im,cmap='gray',aspect='equal')
        ax.axvline(x=math.floor(largeur/4)-l,color='red')
        ax.axvline(x=math.floor(largeur/4)+l,color='red')
        ax.axvline(x=math.floor(2*largeur/4)-l,color='red')
        ax.axvline(x=math.floor(2*largeur/4)+l,color='red')
        ax.axvline(x=math.floor(3*largeur/4)-l,color='red')
        ax.axvline(x=math.floor(3*largeur/4)+l,color='red')
        ax.axhline(y=math.floor(hauteur/3)-l,color='red')
        ax.axhline(y=math.floor(hauteur/3)+l,color='red')
        ax.axhline(y=math.floor(2*hauteur/3)-l,color='red')
        ax.axhline(y=math.floor(2*hauteur/3)+l,color='red')
        ax.plot(self.bary[0],self.bary[1],'b*')
        plt.show()
    
    def rotate(self,angle):
        Rot = cv2.getRotationMatrix2D((math.floor(self.im.shape[1]/2),math.floor(self.im.shape[0]/2)), angle, 1)
        return(cv2.warpAffine(self.im,Rot,(self.im.shape[1],self.im.shape[0])))
        
    def rotate90(self):
        return(np.rot90(self.im))
    
    def cut(self,im): 
        if self.bac==[[0,0],[0,0]]:
            print("bac non initialisé impossible de couper")
        else:
            return im[ self.bac[0][1]:self.bac[1][1] , self.bac[0][0]:self.bac[1][0] ]
    
    def resize(self,scale):
        self.im = cv2.resize(self.im, (0,0), 0, scale, scale, cv2.INTER_AREA)
    
    def retrieveMouse(self):
        #faire une étoile et s'arrêter dès qu'on trouve de la souris
        b=self.bary
        g=self.bary
        d=self.bary
        h=self.bary
        dhg=self.bary
        dhd=self.bary
        dbd=self.bary
        dbg=self.bary
        
        critdroite=d[0]<self.im.shape[1]-1
        critbas=b[1]<self.im.shape[0]-1
        critgauche=g[0]>0
        crithaut=h[1]>0
        
        while(critbas or critdroite or crithaut or critgauche):
            if critbas:
                if (self.im[b[1]][b[0]]==1):
                    return(b)
                if critdroite:
                    if (self.im[dbd[1]][dbd[0]]==1):
                        return(dbd)
                if critgauche:
                    if (self.im[dbg[1]][dbg[0]]==1):
                        return(dbg)
            if crithaut:
                if (self.im[h[1]][h[0]]==1):
                    return(h)
                if critdroite:
                    if (self.im[dhd[1]][dbd[0]]==1):
                        return(dhd)
                if critgauche:
                    if (self.im[dhg[1]][dhg[0]]==1):
                        return(dhg)
            if critdroite:
                 if (self.im[d[1]][d[0]]==1):
                     return(d)
            if critgauche:
                if (self.im[g[1]][g[0]]==1):
                    return(g)
            
            b=[b[0],b[1]+1]
            g=[g[0]-1,g[1]]
            d=[d[0]+1,d[1]]
            h=[h[0],h[1]-1]
            dhg=[dhg[0]-1,dhg[1]-1]
            dhd=[dhd[0]+1,dhd[1]-1]
            dbd=[dbd[0]+1,dbd[1]+1]
            dbg=[dbg[0]-1,dbg[1]+1]            
            critdroite=d[0]<self.im.shape[1]-1
            critbas=b[1]<self.im.shape[0]-1
            critgauche=g[0]>0
            crithaut=h[1]>0
        print("Mouse couldn\'t be retrieved")
        self.showFrame(5)

        return self.bary
        
    def actualiseBary(self):
        oldbary=[self.bary[0],self.bary[1]]           
        bas=[oldbary[0],oldbary[1]]
        haut=[oldbary[0],oldbary[1]]
        droit=[oldbary[0],oldbary[1]]
        gauche=[oldbary[0],oldbary[1]]    
        while (bas[1]<self.im.shape[0]-1) and (self.im[bas[1]+1][bas[0]]==1):
            bas[1]=bas[1]+1           
        while (haut[1]>0) and (self.im[haut[1]-1][haut[0]]==1):
            haut[1]=haut[1]-1              
        while (droit[0]<self.im.shape[1]-1) and (self.im[droit[1]][droit[0]+1]==1):
            droit[0]=droit[0]+1            
        while (gauche[0]>0) and (self.im[gauche[1]][gauche[0]-1]==1):
            gauche[0]=gauche[0]-1         
        self.bary[0]=math.floor((droit[0]+gauche[0])/2)
        self.bary[1]=math.floor((bas[1]+haut[1])/2)        
        diaghd=[self.bary[0],self.bary[1]]
        diaghg=[self.bary[0],self.bary[1]]
        diagbd=[self.bary[0],self.bary[1]]
        diagbg=[self.bary[0],self.bary[1]]        
        while (diaghg[0]>0) and (diaghg[1]>0) and (self.im[diaghg[1]-1][diaghg[0]-1]==1):
            diaghg[0]=diaghg[0]-1
            diaghg[1]=diaghg[1]-1
        while (diaghd[0]<self.im.shape[1]-1) and (diaghd[1]>0) and (self.im[diaghd[1]-1][diaghd[0]+1]==1):
            diaghd[0]=diaghd[0]+1
            diaghd[1]=diaghd[1]-1 
        while (diagbd[0]<self.im.shape[1]-1) and (diagbd[1]<self.im.shape[0]-1) and (self.im[diagbd[1]+1][diagbd[0]+1]==1):
            diagbd[0]=diagbd[0]+1
            diagbd[1]=diagbd[1]+1
        while (diagbg[0]>0) and (diagbg[1]<self.im.shape[0]-1) and (self.im[diagbg[1]+1][diagbg[0]-1]==1):
            diagbg[0]=diagbg[0]-1
            diagbg[1]=diagbg[1]+1
        self.bary[0] = math.floor((diagbg[0]+diagbd[0]+diaghd[0]+diaghg[0])/4)
        self.bary[1] = math.floor((diagbg[1]+diagbd[1]+diaghd[1]+diaghg[1])/4)
        


