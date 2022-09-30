# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 23:11:59 2022

@author: max_n
"""

from PIL import Image
import numpy as np
from math import sqrt

#convert to grayscale
im = np.array(Image.open(r"grayscale.jpg").convert('L'))
ar = np.array(im)

#create a mask with 1's containing a square of 0's
mask = np.ones((1000, 1000))
for i in range(1, 50):
    mask[i][250:300] = 0
#save masked
masked_save = Image.fromarray(mask*255)
masked_save = masked_save.convert('L')
masked_save.save("masked_2.png")

#overlay mask
masked = mask*ar


#D and h values
D = .5
h = 1


for k in range(1, 1001):
    for i in range(1, 50):
        for j in range(250, 300):
            #Laplace equation
            #masked[i][j] = (masked[i-1][j] + masked[i+1][j] + masked[i][j-1] + masked[i][j+1])/4
            
            
            #Diffusion equation
            if k == 1 and j != 300 and i != 50:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i][j-1] - (4-2)*masked[i][j])
            elif k == 1 and j == 300 and i != 50:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i][j-1] + masked[i][j+1] - (4-1)*masked[i][j])
            elif k == 1 and j != 300 and i == 50:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i+1][j] + masked[i][j-1] - (4-1)*masked[i][j])           
            else:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i+1][j] + masked[i][j-1] + masked[i][j+1] - 4*masked[i][j])
                

restored = Image.fromarray(masked)
restored.show()
