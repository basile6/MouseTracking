# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

class Grid():
    
    def __init__(self):
        self.grid=[[0,0,0],[0,0]]
        self.active=[ [[False,False],[False,False],[False,False]] , [[False,False],[False,False]] ]
    
    def plotGrid(self):
        fig=plt.figure(figsize=(6,4))
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.axvline(x=0,color='black',linewidth=10)
        ax.axvline(x=10,color='red')
        ax.axvline(x=20,color='red')
        ax.axvline(x=30,color='red')
        ax.axvline(x=40,color='black',linewidth=10)
        ax.axhline(y=0,color='black',linewidth=10)
        ax.axhline(y=10,color='red')
        ax.axhline(y=20,color='red')
        ax.axhline(y=30,color='black',linewidth=10)
        
        ax.annotate(self.grid[0][0],xy=(10, 26),xytext=(11,26), fontsize=16,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[0][0][0],xy=(10, 2),xytext=(5.5,2), fontsize=12,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[0][0][1],xy=(10, 2),xytext=(10.5,2), fontsize=12,arrowprops=dict(arrowstyle="-"))

        ax.annotate(self.grid[0][1],xy=(20, 26),xytext=(21,26), fontsize=16,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[0][1][0],xy=(20, 2),xytext=(15.5,2), fontsize=12,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[0][1][1],xy=(20, 2),xytext=(20.5,2), fontsize=12,arrowprops=dict(arrowstyle="-"))

        ax.annotate(self.grid[0][2],xy=(30, 26),xytext=(31,26), fontsize=16,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[0][2][0],xy=(30, 2),xytext=(25.5,2), fontsize=12,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[0][2][1],xy=(30, 2),xytext=(30.5,2), fontsize=12,arrowprops=dict(arrowstyle="-"))

        ax.annotate(self.grid[1][0],xy=(5, 20),xytext=(4,21), fontsize=16,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[1][0][0],xy=(35, 20),xytext=(35,21), fontsize=12,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[1][0][1],xy=(35, 20),xytext=(35,18), fontsize=12,arrowprops=dict(arrowstyle="-"))
        
        ax.annotate(self.grid[1][1],xy=(5, 10),xytext=(4,11), fontsize=16,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[1][1][0],xy=(35, 10),xytext=(35,11), fontsize=12,arrowprops=dict(arrowstyle="-"))
        ax.annotate(self.active[1][1][1],xy=(35, 10),xytext=(35,8), fontsize=12,arrowprops=dict(arrowstyle="-"))

        ax.set_xlim(0,40)
        ax.set_ylim(0,30)
        plt.show()
        
    def add(self,t):
        self.grid[0]=[self.grid[0][i]+t[0][i] for i in range(3)]
        self.grid[1]=[self.grid[1][i]+t[1][i] for i in range(2)]
        
    def total(self):
        tot=0
        for i in self.grid:
            for j in i:
                tot=tot+j
        return tot