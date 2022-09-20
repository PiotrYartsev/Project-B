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
print(len(ar))
#create a mask with 1's containing a square of 0's
mask = np.ones((1000, 1000))
for i in range(0, 50):
    mask[i][250:260] = 0
for i in range(200, 500):
    mask[i][250:260] = 0
    mask[i][500:530] = 0



#overlay mask
masked = mask*ar
ruined = Image.fromarray(masked)
ruined2=ruined.convert("L")
ruined2.show()
ruined2.save("ruined.jpg")

#D and h values
D = .5
h = 1
b=[]
#print(max(range(len(mask))))
for i in range(len(mask)):
    #print(i)
    #print(max(range(len(mask[i]))))
    for j in range(0,len(mask[i])):
        
        
        if mask[i][j]==0:
            n=0
            #if at edge/Neumann boundaries
            if i-1<0:
                pass
            if i+1>len(mask):
                pass
            if j-1<0:
                pass

           
            if j-1<len(mask[i]):
                pass

            #if next to other cell
            if mask[i-1][j]==0:
                pass
            
            if mask[i+1][j]==0:
                pass
            if mask[i][j-1]==0:
                pass
            if mask[i][j+1]==0:
                pass

                
            
                

            masked[i][j]=

     
                



            

"""
for k in range(0, 1000):
    for i in range(0, 50):
        for j in range(250, 300):
            #Laplace equation
            #masked[i][j] = (masked[i-1][j] + masked[i+1][j] + masked[i][j-1] + masked[i][j+1])/4
            
            
            #Diffusion equation
            if k == 0 and j != 300 and i != 50:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i][j-1] - (4-2)*masked[i][j])
            elif k == 0 and j == 300 and i != 50:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i][j-1] + masked[i][j+1] - (4-1)*masked[i][j])
            elif k == 0 and j != 300 and i == 50:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i+1][j] + masked[i][j-1] - (4-1)*masked[i][j])           
            else:
                masked[i][j] = masked[i][j] + D*h*(masked[i-1][j] + masked[i+1][j] + masked[i][j-1] + masked[i][j+1] - 4*masked[i][j])
                
"""

restored = Image.fromarray(masked)
restored=restored.convert('L')
restored.show()
restored.save("restored.jpg")


def error_measure(mask, original, restored):
    positions=[]
    for i in range(len(mask)):
    #print(i)
        for j in range(0,len(mask[i])):
            if mask[i][j]==0:
                positions.append((i,j))
    value_over_original = 0
    for p in positions:
        value_over_original += original[p[0]][p[1]]
        #print(value_over_original)
    average_value_over_original = value_over_original/len(positions)
    #print(average_value_over_original)
    sigma_squared = 0
    for p in positions:
        sigma_squared += (original[p[0]][p[1]]-average_value_over_original)**2
    sigma_squared = sigma_squared/(len(positions)-1)
    #print(sigma_squared)

    Chi_squared_list = []
    for p in positions:
        Chi_squared_list.append((original[p[0]][p[1]]-restored[p[0]][p[1]])**2)
    Chi_squared = sum(Chi_squared_list)*1/len(positions)/sigma_squared
    print(Chi_squared)
error_measure(mask, ar, masked)