# -*- coding: utf-8 -*-
import ThreadVid
import IFrame
 

import matplotlib.pyplot as plt
import cv2
import math
import numpy as np
import Thresholding.Binary 

## L'utilisateur choisit la vidéo à analyser #####################################################################
import tkinter as tk
from tkinter.filedialog import askopenfilename
root = tk.Tk()
nameVid = askopenfilename(title="Ouvrir la vidéo")
root.withdraw() 
##################################################################################################################

## paramètres ####################################################################################################
scale=1 #multiplie la taille de l'image par scale (à abaisser pour vidéos haute résolution)

fps=15 #frame per second de la video

largeurbande_m=0.01 #la largeur entre les lignes de la grid en cm

lbac=0.6 #longueur du bac où sont les souris
##################################################################################################################

cap = cv2.VideoCapture(nameVid)
ret, im = cap.read() 

## Utilisateur choisit le nombre de souris à analyser ############################################################
plt.imshow(im,cmap='gray',aspect='equal')
plt.show()
print("nombre de souris à analyser")
t=input()
nbac=int(t)   
##################################################################################################################

satisfiedUser=False
introFrame=IFrame.IFrame(im)    
introFrame.resize(scale)  

## Utilisateur choisit s'il il veut tourner l'image à 90 (change les dimensions de l'image) ######################
horizontal=True
plt.imshow(im,cmap='gray',aspect='equal')
plt.show()
print("voulez vous tourner à 90° la vidéo? (les bacs doivent être horizontaux) ATTENTION ROTATION SENS TRIGO (y/n)")
answer=input()
if answer=='y':
    introFrame.im=introFrame.rotate90()
    horizontal=False
##################################################################################################################
    
## Utilisateur choisit quand commencer l'analyse #################################################################
debut=0
satisfiedUser=False
while satisfiedUser==False:
    plt.imshow(introFrame.im,cmap='gray',aspect='equal')
    plt.show()
    print("voulez vous avancer la vidéo? (y/n)")
    answer=input()
    if answer=='y':
        print("Entrez le nombre de secondes à passer:")
        t=input()
        for i in range(fps*int(t)):
            ret,introFrame.im=cap.read()
        debut=debut+int(t)
        if horizontal==False:
            introFrame.im=introFrame.rotate90()
        plt.imshow(introFrame.im,cmap='gray',aspect='equal')
        plt.show()
        print("Voulez vous continuer à avancer la vidéo? (y/n)")
        answer=input()
    if answer=='n':
        satisfiedUser=True
##################################################################################################################
        
        
## Utilisateur entre des petits angles de correction pour mettre les bacs droits #################################
satisfiedUser=False    
angle = 0
while satisfiedUser==False:
    plt.imshow(introFrame.im,cmap='gray',aspect='equal')
    plt.show()
    print("voulez vous tourner l'image? (y/n)")
    answer=input()
    if answer=='y':
        print("entrez l'angle de rotation en degré: (+ => vers la gauche)")
        d=input()
        im=introFrame.rotate(int(d))
        angle = int(d)
        plt.imshow(im,cmap='gray',aspect='equal')
        plt.show()
        print("voulez vous tourner l'image une nouvelle fois?")
        answer=input()
    if answer=='n':
        satisfiedUser=True
##################################################################################################################

th=dict()
im=introFrame.im

## Pour chaque souris, l'utilisateur choisit les limites du bac, le seuil et la pos de départ de la souris #######
for i in range(nbac):
    
    introFrame.im=im
    introFrame.clicks=list()
    introFrame.im=introFrame.rotate(angle)
    introFrame.getUserClicks("le bac a considerer: diaghautgauche puis diagbasdroite")
    introFrame.bac=[introFrame.clicks[0],introFrame.clicks[1]]
    introFrame.cut()
    introFrame.getUserClicks("barycentre de la souris")
    bary=introFrame.clicks[2]
    
    satisfiedUser=False 
    
    seuil=110 #seuil par défaut
    
    while satisfiedUser==False:
        plt.imshow(Thresholding.Binary.SeuillageBinaire(cv2.cvtColor(introFrame.im, cv2.COLOR_BGR2GRAY),seuil),cmap='gray',aspect='equal')
        plt.show()
        print("voulez vous changer le seuil? (y/n)")
        answer=input()
        if answer=='y':
            print("entrez le seuil: (0=noir 255=blanc). La souris doit être blanche et avoir la même forme qu'en vrai. Le background doit lui être noir. Entrez le nombre le plus haut possible avec un background noir")
            d=input()
            seuil = int(d)
            plt.imshow(Thresholding.Binary.SeuillageBinaire(cv2.cvtColor(introFrame.im, cv2.COLOR_BGR2GRAY),seuil),cmap='gray',aspect='equal')
            plt.show()
            print("continuer à changer le seuil?")
            answer=input()
        if answer=='n':
            satisfiedUser=True
    
    echelle=lbac/(np.abs(introFrame.bac[0][0]-introFrame.bac[1][0]))
    
    print("echelle")
    print(echelle)   
    largeurbande_pix=math.floor(largeurbande_m/echelle)
    print("la largeur des bandes")
    print(largeurbande_pix)
    
    th[str(i)]=ThreadVid.ThreadVid(nameVid,introFrame.bac,bary,scale,angle,debut*fps,echelle,largeurbande_pix,seuil,horizontal,fps)
    print(th[str(i)])
    th[str(i)].start()  
##################################################################################################################


for i in range(nbac):
    th[str(i)].join()
    
for i in range(nbac):
    print("thread " + str(i) + " fini, résultats:")    
    print(th[str(i)].grid.plotGrid())
    print("distance totale parcourue en pixel")
    print(th[str(i)].dparc)
    print("estimation correspondante en m")
    print(th[str(i)].dparc*echelle)
    print("nombre de croisements avec la grid")
    print(th[str(i)].grid.total())

    

    


