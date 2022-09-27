# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 23:11:59 2022

@author: max_n
"""
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

def add_mask_of_text(ar):
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
    #mask_save.save("mask_text.png")


    #overlay mask
    masked=ar*mask
    masked_again_imimage = Image.fromarray(masked)

    #save image with mask overlayied on it
    masked_again_imimage_save=masked_again_imimage.convert("L")
    #masked_again_imimage_save.save("masked_with_text.png")
    return masked, mask

#generating the mas kand overlayingit on top of 
masked,mask=add_mask_of_text(ar)
masked1=masked


#anisotropic diffusion constant
def diffusion(i,j):
    K = 300 #value that is guessed basically (300 is pretty good)
    div = (masked[i+1][j] - masked[i][j])**2 + (masked[i][j+1] - masked[i][j])**2
    c = np.exp(-(div/K)**2)
        
    return c


def restore_image(masked1,mask,iteration):
    masked=masked1
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
            if k==-1: #changed just to ignore no flux
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


                #masked[i][j] =masked[i][j]+ D*h*(u_1_0+u__1_0+u_0_1+u_0__1-(4-n)*masked[i][j])
                """masked[i][j] = masked[i][j] + (((1/2)*(diffusion(i+1, j) + diffusion(i,j)))*(u__1_0 - masked[i][j])-((1/2)*(diffusion(i-1, j) + diffusion(i, j)))\
                        *(masked[i][j]-u_1_0)) + (((1/2)*(diffusion(i, j+1) + diffusion(i,j)))*(u_0__1 - masked[i][j])-((1/2)*(diffusion(i, j-1) + diffusion(i, j)))\
                                                                          *(masked[i][j]-u_0_1))"""
                
            else: 
                #masked[i][j] = masked[i][j] + D*h*(masked[i-1][j]+masked[i+1][j]+masked[i][j-1]+masked[i][j+1] - 4*masked[i][j])
                
                #anisotropic equation
                masked[i][j] = masked[i][j] + (((1/2)*(diffusion(i+1, j) + diffusion(i,j)))*(masked[i+1][j] - masked[i][j])-((1/2)*(diffusion(i-1, j) + diffusion(i, j)))\
                        *(masked[i][j]-masked[i-1][j])) + (((1/2)*(diffusion(i, j+1) + diffusion(i,j)))*(masked[i][j+1] - masked[i][j])-((1/2)*(diffusion(i, j-1) + diffusion(i, j)))\
                                                                          *(masked[i][j]-masked[i][j-1]))


    return masked

#running the numerical method
masked=restore_image(masked,mask,100)
restored = Image.fromarray(masked)
restored.show()

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

print("Calculate the error\n\n")
print(error_measure(mask, ar, masked))
masked2=masked1
error_from_steps=[]

"""
stepsize=np.logspace(0,3,30)
print(stepsize)

setpsize2=np.linspace(1,1000,10)
maxvalud=len(stepsize)
for i in (stepsize):
    i=int(i)
    masked1=ar*mask
    
    print("restoring for stepsize {}".format(i))
    masked1=restore_image(masked1,mask,i)
    if i in setpsize2:
        #save image of the restored image
        restored = Image.fromarray(masked1)
        #restored.show()           
        restored2=restored.convert("L")
        restored2.save("{}_new_method_restored.png".format(i))
    print("calculating the error")
    error=error_measure(mask, ar, masked1)
    error_from_steps.append(error)
    print(error)
    print("\n\n")
plt.plot(stepsize,error_from_steps)

#make a logorithim plot
plt.grid()
plt.ylim(0)
plt.xscale("log")
plt.xlabel("Number of steps")
plt.ylabel("Chi^2 error")
plt.title("Chi^2 error as a function of the number of steps")
plt.savefig("error_vs_steps.png", bbox_inches='tight')
plt.show()
"""