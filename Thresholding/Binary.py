import numpy as np

def SeuillageBinaire(im,seuil):
    im = 1*(im<seuil)
    return(im)

