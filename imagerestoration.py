# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 23:11:59 2022

@author: max_n
"""

from PIL import Image
import numpy as np
from math import sqrt
import numpy
from tqdm import tqdm
#convert to grayscale
im = np.array(Image.open(r"grayscale.jpg").convert('L'))
ar = np.array(im)
#print(numpy.max(ar))
#print(len(ar))
#create a mask with 1's containing a square of 0's
mask = np.ones((1000, 1000))
for i in range(0, 50):
    mask[i][250:260] = 0
for i in range(200, 250):
    mask[i][400:430] = 0



mask_show = Image.fromarray(mask*255)
mask_show.show()
#overlay mask
masked = mask*ar
ruined = Image.fromarray(masked)
ruined.show()


#D and h values
D = .5
h = 1





for k in tqdm(range(1)):
    
    for i in range(len(masked)):
        for j in range(len(masked[i])):
            #print(i,j)
            if mask[j][i]==0:
                if k==0:
                    n=0
                    len_mask=len(mask)
                    #print(len_mask)
                    len_mask_i=len(mask[i])
                    #print(len_mask_i)
                    u_0__1 = masked[i][j-1]
                    u_0_1 = masked[i][j+1]

                    u_1_0 = masked[i+1][j]
                    u__1_0 = masked[i-1][j]
                    
                    if i+1 >= len_mask_i:
                        print(i+1)
                        u_1_0=0
                        n+=1

                    if i-1 < 0:
                        n+=1
                        u__1_0=0

                    if j+1 >= len_mask:
                        print(j+1)
                        u_0_1=0
                        n+=1

                    if j-1 < 0:
                        u_0__1=0
                        n+=1


                    masked[i][j] =masked[i][j]+ D*h*(u_1_0+u__1_0+u_0_1+u_0__1-(4-n)*masked[i][j])
                    
                else:
                    masked[i][j] = masked[i][j] + h*(D*masked[i-1][j]+masked[i+1][j]+masked[i][j-1]+masked[i][j+1] - D*4*masked[i][j])



restored = Image.fromarray(masked)
restored.show()           
                



            


"""
for k in range(0, 100):
    for i in range(0, 50):
        for j in range(250, 260):
            #Laplace equation
            #masked[i][j] = (masked[i-1][j] + masked[i+1][j] + masked[i][j-1] + masked[i][j+1])/4
            
            
            #Diffusion equation


            if k == 0 and j != 260 and i != 50:
                masked[i][j] = masked[i][j] + h*(D*masked[i-1][j] + D*masked[i][j-1] - D*(4-2)*masked[i][j])
            elif k == 0 and j == 260 and i != 50:


                masked[i][j] = masked[i][j] + h*(D*masked[i-1][j] + D*masked[i][j-1] + D*masked[i][j+1] - D*(4-1)*masked[i][j])
            elif k == 0 and j != 260 and i == 50:


                masked[i][j] = masked[i][j] + h*(D*masked[i-1][j] + D*masked[i+1][j] + D*masked[i][j-1] - D*(4-1)*masked[i][j])           
            else:


                masked[i][j] = masked[i][j] + h*(D*masked[i-1][j] + D*masked[i+1][j] + D*masked[i][j-1] + D*masked[i][j+1] - D*4*masked[i][j])
                

restored = Image.fromarray(masked)
restored.show()
"""

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



