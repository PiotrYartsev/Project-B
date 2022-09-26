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

def add_mask_of_text(text,ar,number):
    #Create a mask of 1
    whiteblankimage = np.ones((1000, 1000))
    #Add text with color 0 to the image
    cv2.putText(whiteblankimage, text='Piotr', org=(300,150),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
                thickness=15, lineType=cv2.LINE_AA)
    cv2.putText(whiteblankimage, text='AND', org=(300,350),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
                thickness=15, lineType=cv2.LINE_AA)
    cv2.putText(whiteblankimage, text='Max', org=(300,550),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
                thickness=15, lineType=cv2.LINE_AA)
    cv2.putText(whiteblankimage, text='Fix', org=(300,750),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
                thickness=15, lineType=cv2.LINE_AA)
    cv2.putText(whiteblankimage, text='Images', org=(300,950),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0),
                thickness=15, lineType=cv2.LINE_AA)

    #make image to array
    mask=np.array(whiteblankimage)
    mask_save=Image.fromarray(mask*255)
    mask_save=mask_save.convert("L")
    mask_save.save("{}_mask_text.png".format(number))


    #overlay mask
    masked=ar*mask
    masked_again_imimage = Image.fromarray(masked)

    #save image with mask overlayied on it
    masked_again_imimage_save=masked_again_imimage.convert("L")
    masked_again_imimage_save.save("masked_with_text.png")
    return masked, mask

#generating the mas kand overlayingit on top of 
masked,mask=add_mask_of_text("Piotr",ar,1)
masked1=masked

def restore_image(masked,mask,number,iteration):
    #D and h values
    D = .5
    h = 1

    #get position of the mask
    positions=[]

    for i in  tqdm(range(len(mask))):
        for j in range(len(mask[i])):
            if mask[i][j]==0:
                positions.append((i,j))

    #run the numerical method
    len_mask=len(mask)
    len_mask_i=len(mask[0])
    for k in tqdm(range(iteration)):
        
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
    #restored.show()           
    restored2=restored.convert("L")
    restored2.save("{}_restored.png".format(number))
    return masked

#running the numerical method
masked=restore_image(masked,mask,1_1,100)

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
    for p in tqdm(positions):
        Chi_squared_list.append((original[p[0]][p[1]]-restored[p[0]][p[1]])**2)
    Chi_squared = sum(Chi_squared_list)*1/len(positions)/sigma_squared
    return Chi_squared
    #print(Chi_squared)

print("Calculate the error")
#error_measure(mask, ar, masked)

error_from_steps=[]
stepsize=np.linspace(1,100,10)
for i in (stepsize):
    i=int(i)
    print(i)
    print("restoring for stepsize {}".format(i))
    masked=restore_image(masked1,mask,i,i)
    print("calculating the error")
    error=error_measure(mask, ar, masked)
    error_from_steps.append(error)
    print(error)
plt.plot(stepsize,error_from_steps)
plt.show()