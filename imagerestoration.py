# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 23:11:59 2022

@author: max_n
"""
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from math import sqrt
import numpy
from tqdm import tqdm
import cv2
#convert to grayscale

im = np.array(Image.open(r"grayscale.jpg").convert('L'))
ar = np.array(im)





#create a mask with 1's containing a square of 0's
mask = np.ones((1000, 1000))
for i in range(0, 50):
    mask[i][250:260] = 0
for i in range(200, 250):
    mask[i][400:430] = 0






"""
#save image of the mask used
mask_show = Image.fromarray(mask*255)
mask_show2=mask_show.convert("L")
mask_show2.save("mask.png")
#mask_show.show()

#overlay mask
masked = mask*ar
ruined = Image.fromarray(masked)
ruined.show()
ruined2=ruined.convert("L")
ruined2.save("ruined.png")
"""

#add text to mask
mask2 = np.ones((1000, 1000))
text = "This is a test"


whiteblankimage = 1 * np.ones(shape=[1000, 1000], dtype=np.uint8)


cv2.putText(whiteblankimage, text='Ruined', org=(300,200),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
            thickness=5, lineType=cv2.LINE_AA)
"""
cv2.putText(whiteblankimage, text='Ruined', org=(300,400),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
            thickness=5, lineType=cv2.LINE_AA)
cv2.putText(whiteblankimage, text='Ruined', org=(300,600),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
            thickness=5, lineType=cv2.LINE_AA)
cv2.putText(whiteblankimage, text='Ruined', org=(300,800),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
            thickness=5, lineType=cv2.LINE_AA)
"""
#overlay mask
mask=np.array(whiteblankimage)

masked=ar*mask
masked_again_imimage = Image.fromarray(masked)
masked_again_imimage.show()






#D and h values
D = .5
h = 1

positions=[]
for i in  tqdm(range(len(mask))):
    for j in range(len(mask[i])):
        if mask[i][j]==0:
            positions.append((i,j))

len_mask=len(mask)
len_mask_i=len(mask[0])
for k in tqdm(range(100)):
    
    for p in positions:
        i=p[0]
        j=p[1]
        if k==0:
            n=0

            u_0__1 = masked[i][j+1]
            u_0_1 = masked[i][j-1]

            u_1_0 = masked[i-1][j]
            u__1_0 = masked[i+1][j]
            
            if not i+1 >= len_mask_i and not j+1 >= len_mask:
                u__1_0=0
                u_0__1=0
                n=2

            if j+1 >= len_mask and not i+1 >= len_mask_i:
                u_0__1=0
                n=1

            if not j+1 >= len_mask and i+1 >= len_mask_i:
                u__1_0=0

                n=1
            else:
                n=0


            masked[i][j] =masked[i][j]+ D*h*(u_1_0+u__1_0+u_0_1+u_0__1-(4-n)*masked[i][j])
            
        else:
            masked[i][j] = masked[i][j] + D*h*(masked[i-1][j]+masked[i+1][j]+masked[i][j-1]+masked[i][j+1] - 4*masked[i][j])


#save image of the restored image
restored = Image.fromarray(masked)
restored.show()           
restored2=restored.convert("L")
restored2.save("restored.png")
                

#calculate the error
def error_measure(mask, original, restored):
    positions=[]
    for i in range(len(mask)):
        for j in range(0,len(mask[i])):
            if mask[i][j]==0:
                positions.append((i,j))

    value_over_original = 0

    for p in positions:
        value_over_original += original[p[0]][p[1]]
    average_value_over_original = value_over_original/len(positions)
    sigma_squared = 0

    for p in positions:
        sigma_squared += (original[p[0]][p[1]]-average_value_over_original)**2
    sigma_squared = sigma_squared/(len(positions)-1)

    Chi_squared_list = []
    for p in positions:
        Chi_squared_list.append((original[p[0]][p[1]]-restored[p[0]][p[1]])**2)
    Chi_squared = sum(Chi_squared_list)*1/len(positions)/sigma_squared
    print(Chi_squared)
error_measure(mask, ar, masked)



