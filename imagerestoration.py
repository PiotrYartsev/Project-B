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
#ruined = Image.fromarray(masked)
#ruined.show()


#D and h values
D = .5
h = 1

#print(max(range(len(mask))))
for i in range(len(mask)):
    #print(i)
    #print(max(range(len(mask[i]))))
    for j in range(0,len(mask[i])):
        
        
        if mask[i][j]==0:

            n=0
            if i+1 > len(mask):
                u_1_0=0
                n+=1
            else:
                u_1_0 = masked[i+1][j]
                
            if i-1 < 0:
                n+=1

                u__1_0=0
            else:
                u__1_0 = masked[i-1][j]

            if j+1 > len(mask[i]):
                u_0_1=0
                n+=1
            else:
                u_0_1 = masked[i][j+1]
        


            if j-1 < 0:
                u_0__1=0
                n+=1
            else:
                u_0__1 = masked[i][j-1]
            if n==4:
                u_0_0=0
            else:
                u_0_0 = masked[i][j]

            masked[i][j] =masked[i][j]+ D*h*(u_1_0+u__1_0+u_0_1+u_0__1-(4-n)*u_0_0)



restored = Image.fromarray(masked)
#restored.show()           

                



            

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
restored.show()


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