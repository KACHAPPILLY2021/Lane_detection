# Importing libraries
import cv2
import numpy as np 
from matplotlib import pyplot as plt
import time

start = time.time()

# Loop for going through given dataset
for a in range(25):

# Reading image as grayscale
    img = cv2.imread("data/"+str(a)+".png", 0)
    img1 = img.copy()
    print("Frame : "+str(a))
# Splitting the array into equal horizontal sub arrays
    slices = np.array_split(img1 , 8 , axis =0)
# Splitting each horizontal array into equal vertical arrays
    packet = [np.array_split(part , 8 , axis =1) for part in slices]

# Traversing through each block
    for i in range(len(packet)) :
        for j in range(len(packet[i])) :
        # numpy array for storing number of pixels with same intensity (bin size = 255)
            intensity_count = np.zeros((1 , 256) )

            patch = packet[i][j]
        # Getting height and width of current block
            height , width=patch.shape
            size=width*height
        # Checking intensity of each pixel in image and updating the corresponding intensity counter
            for x in range(height):
                for y in range(width):
                    intensity_count[0 , patch[x][y]] = intensity_count[0 , patch[x][y]] + 1
        # determining fraction of pixels for a given intensity to total number of pixels in the current block
            pdf = intensity_count/size 

        #initialize array for cumulative distribution function 
            cdf=np.zeros((1 , 256) )
            total=0
        # Determining the cumulative distribution for a given intensity
            for k in range(256):
                total=total+pdf[0 , k]
                cdf[0 , k] = total
        # Getting new intensity values by multiplying cdf with 255
            tr=np.round(cdf*255)
        # Assigning new intensity to the block
            for x in range(height):
                for y in range(width):
                    patch[x][y] = tr[0 , patch[x][y] ]


# Joining all blocks together
    result = np.block(packet)
# concatanate image Vertically
    Verti = np.concatenate((img, result), axis=0)
    cv2.imshow("Before and after Adaptive equalization", Verti)

    end = time.time()
    print("time taken to run the code"+ " : " + str(end-start)+ " seconds ")  

    cv2.waitKey(20)

cv2.destroyAllWindows()

