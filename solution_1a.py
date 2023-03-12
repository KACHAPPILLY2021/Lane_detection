# Importing libraries
import cv2
import numpy as np 
from matplotlib import pyplot as plt
import time

start = time.time()

# Loop for going through given dataset
for i in range(25):

# Reading image as grayscale
    img = cv2.imread("data/"+str(i)+".png", 0)

    img1 = img.copy()

# numpy array for storing number of pixels with same intensity (bin size = 255)
    intensity_count = np.zeros((1 , 256) )

    print("Frame : "+str(i))
# Getting height and width of given frame
    height , width=img.shape
    size=width*height

# Checking intensity of each pixel in image and updating the corresponding intensity counter
    for x in range(height):
        for y in range(width):
            intensity_count[0 , img[x][y]] = intensity_count[0 , img[x][y]] + 1

# determining fraction of pixels for a given intensity to total number of pixels 
    pdf = intensity_count/size 

#initialize array for cumulative distribution function 
    cdf=np.zeros((1 , 256) )
    total=0
# Determining the cumulative distribution for a given intensity
    for i in range(256):
        total=total+pdf[0 , i]
        cdf[0 , i] = total
# Getting new intensity values by multiplying cdf with 255
    tr=np.round(cdf*255)
# Assigning new intensity to the image
    for x in range(height):
        for y in range(width):
            img1[x][y] = tr[0 , img1[x][y] ]

    # concatanate image Vertically
    Verti = np.concatenate((img, img1), axis=0)
    cv2.imshow("Final Output", Verti)


    end = time.time()
    print("time taken to run : "+  str(end-start)+ " seconds ")  

    cv2.waitKey(20)

    

cv2.destroyAllWindows()