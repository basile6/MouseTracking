# -*- coding: utf-8 -*-
import threading
import Frame
import Grid

import cv2
import numpy as np
import math


class ThreadVid(threading.Thread):
    
    def __init__(self,nom_video,bac,bary,scale,angle,debut,echelle,largeurbande_pix,seuil,horizontal,fps):
        threading.Thread.__init__(self)
        self.nom_video=nom_video
        self.bary=bary
        self.bac=bac
        self.scale=scale
        self.angle=angle
        self.debut=debut
        self.echelle=echelle
        self.l_pix=largeurbande_pix
        self.seuil=seuil
        self.horizontal=horizontal
        self.fps=fps      
        self.dparc=0
        self.grid=Grid.Grid()
        
    
    def run(self):
        
        oldbary=[self.bary[0],self.bary[1]] 
        
        cap = cv2.VideoCapture(self.nom_video)
        ret, im = cap.read()
        
        for i in range(self.debut):
            ret, im = cap.read()
        
        frame = Frame.Frame(im,self.bary,self.bac,self.angle,self.seuil,self.horizontal)        
        
        cpt=0     
        
        while(cap.isOpened()):
            
            if ret==True:
                im = cv2.resize(im, (0,0), 0, self.scale, self.scale, cv2.INTER_AREA)
                im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
                frame = Frame.Frame(im,frame.bary,self.bac,self.angle,self.seuil,self.horizontal)                                
                frame.mouseActualisation()                  
                self.actualiseGrid(oldbary,frame.bary,frame.im.shape[0],frame.im.shape[1])                        
                self.dparc = self.dparc + np.sqrt( (frame.bary[0]-oldbary[0])**2 + (frame.bary[1]-oldbary[1])**2 )                

## Debug : voir ce qu'il se passe pour chaque Frame ##############################################################
#                print("oldbary-bary")
#                print(oldbary,frame.bary)
#                frame.showFrame(self.l_pix)
#                self.grid.plotGrid()               
##################################################################################################################

                oldbary=[frame.bary[0],frame.bary[1]]
            else:
                break            
            if cpt>self.fps*15*60:
#            if cpt > 2:
                break      
            
            ret, im = cap.read()
            cpt=cpt+1
            
        cap.release()
        cv2.destroyAllWindows()
        
    def actualiseGrid(self,oldbary,bary,hauteur,largeur): 
        res=[[0,0,0],[0,0]]

        x1g=math.floor(largeur/4)-self.l_pix
        x1d=math.floor(largeur/4)+self.l_pix
        x2g=math.floor(largeur*2/4)-self.l_pix
        x2d=math.floor(largeur*2/4)+self.l_pix
        x3g=math.floor(largeur*3/4)-self.l_pix
        x3d=math.floor(largeur*3/4)+self.l_pix
        x4=largeur
        
        y1h=math.floor(hauteur/3)-self.l_pix
        y1b=math.floor(hauteur/3)+self.l_pix
        y2h=math.floor(hauteur*2/3)-self.l_pix
        y2b=math.floor(hauteur*2/3)+self.l_pix
        y3=hauteur
        
        ##cas 1 la souris traverse la bande d'un coup:
        if ThreadVid.CollisionSegSeg(oldbary,bary,[x1g,0],[x1g,y3]) and ThreadVid.CollisionSegSeg(oldbary,bary,[x1d,0],[x1d,y3]):
            self.grid.grid[0][0]=self.grid.grid[0][0]+1
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x2g,0],[x2g,y3]) and ThreadVid.CollisionSegSeg(oldbary,bary,[x2d,0],[x2d,y3]):
            self.grid.grid[0][1]=self.grid.grid[0][1]+1
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x3g,0],[x3g,y3]) and ThreadVid.CollisionSegSeg(oldbary,bary,[x3d,0],[x3d,y3]):
            self.grid.grid[0][2]=self.grid.grid[0][2]+1
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x1g,0],[x1g,y3]):
            if self.grid.active[0][0][1]: ##on était entré par la droite, on est en train de sortir par la gauche
                self.grid.grid[0][0]=self.grid.grid[0][0]+1
                self.grid.active[0][0][1]=False
                self.grid.active[0][0][0]=False
            elif self.grid.active[0][0][0] and bary[0]<x1g: ##on est sorti de la bande
                self.grid.active[0][0][0]=False
            elif self.grid.active[0][0][0]==False and bary[0]>x1g: ##on est rentré dans la bande 
                self.grid.active[0][0][0] = True  
                
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x1d,0],[x1d,y3]):
            if self.grid.active[0][0][0]:##déja entré par la gauche on ressort par la droite: cross
                self.grid.grid[0][0]=self.grid.grid[0][0]+1
                self.grid.active[0][0][1]=False
                self.grid.active[0][0][0]=False
            elif self.grid.active[0][0][1] and bary[0]>x1d: ##on est sorti de la bande
                self.grid.active[0][0][1]=False
            elif self.grid.active[0][0][1]==False and bary[0]<x1d: ##on est rentré dans la bande 
                self.grid.active[0][0][1] = True  
                
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x2g,0],[x2g,y3]):
            if self.grid.active[0][1][1]: ##on était entré par la droite, on est en train de sortir par la gauche
                self.grid.grid[0][1]=self.grid.grid[0][1]+1
                self.grid.active[0][1][1]=False
                self.grid.active[0][1][0]=False
            elif self.grid.active[0][1][0] and bary[0]<x2g: ##on est sorti de la bande
                self.grid.active[0][1][0]=False
            elif self.grid.active[0][1][0]==False and bary[0]>x2g: ##on est rentré dans la bande 
                self.grid.active[0][1][0] = True  
                
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x2d,0],[x2d,y3]):
            if self.grid.active[0][1][0]:##déja entré par la gauche on ressort par la droite: cross
                self.grid.grid[0][1]=self.grid.grid[0][1]+1
                self.grid.active[0][1][1]=False
                self.grid.active[0][1][0]=False
            elif self.grid.active[0][1][1] and bary[0]>x2d: ##on est sorti de la bande
                self.grid.active[0][1][1]=False
            elif self.grid.active[0][1][1]==False and bary[0]<x2d: ##on est rentré dans la bande 
                self.grid.active[0][1][1] = True  
                
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x3g,0],[x3g,y3]):
            if self.grid.active[0][2][1]: ##on était entré par la droite, on est en train de sortir par la gauche
                self.grid.grid[0][2]=self.grid.grid[0][2]+1
                self.grid.active[0][2][1]=False
                self.grid.active[0][2][0]=False
            elif self.grid.active[0][2][0] and bary[0]<x3g: ##on est sorti de la bande
                self.grid.active[0][2][0]=False
            elif self.grid.active[0][2][0]==False and bary[0]>x3g: ##on est rentré dans la bande 
                self.grid.active[0][2][0] = True             
                           
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[x3d,0],[x3d,y3]):
            if self.grid.active[0][2][0]:##déja entré par la gauche on ressort par la droite: cross
                self.grid.grid[0][2]=self.grid.grid[0][2]+1
                self.grid.active[0][2][1]=False
                self.grid.active[0][2][0]=False
            elif self.grid.active[0][2][1] and bary[0]>x3d: ##on est sorti de la bande
                self.grid.active[0][2][1]=False
            elif self.grid.active[0][2][1]==False and bary[0]<x3d: ##on est rentré dans la bande 
                self.grid.active[0][2][1] = True 
                
        
        if ThreadVid.CollisionSegSeg(oldbary,bary,[0,y1h],[x4,y1h]) and ThreadVid.CollisionSegSeg(oldbary,bary,[0,y1b],[x4,y1b]):
            self.grid.grid[1][0]=self.grid.grid[1][0]+1
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[0,y2h],[x4,y2h]) and ThreadVid.CollisionSegSeg(oldbary,bary,[0,y2b],[x4,y2b]):
            self.grid.grid[1][1]=self.grid.grid[1][1]+1
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[0,y1h],[x4,y1h]):
            if self.grid.active[1][0][1]: ##entré par en bas, on sort par en haut: cross
                self.grid.grid[1][0]=self.grid.grid[1][0]+1
                self.grid.active[1][0][0]=False
                self.grid.active[1][0][1]=False
            elif self.grid.active[1][0][0] and bary[1]<y1h: ##on est sorti de la bande
                self.grid.active[1][0][0]=False
            elif self.grid.active[1][0][0]==False and bary[1]>y1h: ##on est rentré dans la bande 
                self.grid.active[1][0][0] = True 
               
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[0,y1b],[x4,y1b]):
            if self.grid.active[1][0][0]: ##entré par en haut, sorti par en bas: cross
                self.grid.grid[1][0]=self.grid.grid[1][0]+1
                self.grid.active[1][0][0]=False
                self.grid.active[1][0][1]=False
            elif self.grid.active[1][0][1] and bary[1]>y1b: ##on est sorti de la bande
                self.grid.active[1][0][1]=False
            elif self.grid.active[1][0][1]==False and bary[1]<y1b: ##on est rentré dans la bande 
                self.grid.active[1][0][1] = True       
        
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[0,y2h],[x4,y2h]):
            if self.grid.active[1][1][1]: ##entré par en bas, sorti par en haut: cross
                self.grid.grid[1][1]=self.grid.grid[1][1]+1
                self.grid.active[1][1][0]=False
                self.grid.active[1][1][1]=False
            elif self.grid.active[1][1][0] and bary[1]<y2h: ##on est sorti de la bande
                self.grid.active[1][1][0]=False
            elif self.grid.active[1][1][0]==False and bary[1]>y2h: ##on est rentré dans la bande 
                self.grid.active[1][1][0] = True          
                
        elif ThreadVid.CollisionSegSeg(oldbary,bary,[0,y2b],[x4,y2b]):
            if self.grid.active[1][1][0]: ##entré par en haut, sorti par en bas: cross
                self.grid.grid[1][1]=self.grid.grid[1][1]+1
                self.grid.active[1][1][0]=False
                self.grid.active[1][1][1]=False
            elif self.grid.active[1][1][1] and bary[1]>y2b: ##on est sorti de la bande
                self.grid.active[1][1][1]=False
            elif self.grid.active[1][1][1]==False and bary[1]<y2b: ##on est rentré dans la bande 
                self.grid.active[1][1][1] = True          
        elif (bary[0]>x1d or bary[0]<x1g) and (bary[0]>x2d or bary[0]<x2g) and (bary[0]>x3d or bary[0]<x3g) and (bary[1]>y1b or bary[1]<y1h) and (bary[1]>y2b or bary[1]<y2h):
            ##si on est pas sur une bande tout doit être false
            
            for i in range(3):
                self.grid.active[0][i]=[False,False]
            self.grid.active[1][0]=[False,False]
            self.grid.active[1][1]=[False,False]  
        
        return(res)
   
    def CollisionDroiteSeg(a,b,o,p):
        ab=[b[0]-a[0],b[1]-a[1]]
        ap=[p[0]-a[0],p[1]-a[1]]
        ao=[o[0]-a[0],o[1]-a[1]]
        if (ab[0]*ap[1]-ab[1]*ap[0])*(ab[0]*ao[1]-ab[1]*ao[0])<=0:
            return True
        return False
    
    def CollisionSegSeg(a,b,o,p):
        if a==b or o==p:
            return False
        if a==o or a==p or b==o or b==p:
            return True
        if a[1]==o[1] and o[1]==p[1] and a[1]==b[1]:
            return False
        if a[0]==o[0] and o[0]==p[0] and a[0]==b[0]:
            return False
        if ThreadVid.CollisionDroiteSeg(a,b,o,p)==False:
            return False
        if ThreadVid.CollisionDroiteSeg(o,p,a,b)==False:
            return False
        return True