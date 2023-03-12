# importing libraries
import cv2
from cv2 import threshold
import numpy as np
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video/problem2.mp4')

# Check if image opened successfully
if (cap.isOpened()== False):
    print("Error opening video file")

# Determining x coordinate for given y coordinate using two point line equation
# Passing one (x,y) point from hough transform and passing slope of line determined from hough points 
def find_x(l , m , y_new):
    return int(((y_new-l[3])/m)+l[2])


# Function to differentiate between dashed lanes and the other unimportant line with same slope sign 
def dashed_find(slope) :

    ii = 0
    # Considering first element of list as dashed
    x = slope[0][0]
    # Going through the list
    for i in range(1 , len(slope)) :

        # Considering all the lines with slope within range of [slope-0.1 to slope+0.1]
        if abs(slope[i][0] - x) < 0.1 :
            ii = ii + 1

    # This if condition means that the chosen line was a dashed lane
    if ii > 0 :
        return x , slope[0][1] 
    # This chooses the next line in list as dashed line( since there is only 1 unwanted line for a given frame )
    else :
        return slope[1][0] , slope[1][1] 

# Function for getting dashed lanes
def lane_type(l , slope_solid) :
    # List to store lines having slope which are opposite in sign to solid lane
    slope = []

    for i in range(1 ,len(l)):
        k = l[i][0]
        # Determining slope of each line
        slope_line = (k[3] - k[1])/(k[2] - k[0])
        # Gets executed when slope of solid is '+ve' and slope of current line is '-ve'
        if slope_solid > 0 and slope_line < 0:
            # Storing lines with '-ve' slope
            t = (slope_line , k)
            slope.append(t)
        # Gets executed when slope of solid is '-ve' and slope of current line is '+ve'    
        if slope_solid < 0 and slope_line > 0:
            # Storing lines with '+ve' slope
            t = (slope_line , k)
            slope.append(t)

    # Gets executed if list has only 1 element
    if len(slope) == 1 :
        return slope[0][0] , slope[0][1]
    elif len(slope) > 1:
        return dashed_find(slope)    


# Read until video is completed
while(cap.isOpened()):
	
# Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == True:
        # ####### FOR INVERTING FRAME #######
        # img_flip_lr = cv2.flip(frame, 1)
        # gray = cv2.cvtColor(img_flip_lr,cv2.COLOR_BGR2GRAY)

        # convert to grayscale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)          
        height , width=gray.shape
        # Applying Gaussian blur to remove noise
        gaus_gray = cv2.GaussianBlur(gray,(7,7),cv2.BORDER_DEFAULT)
        # Edge detection to get lanes
        dst = cv2.Canny(gaus_gray, 165, 235)

        # Hough lines to detect straight lines
        linesP = cv2.HoughLinesP(dst, 1, 1*(np.pi / 180), 24, None, 14, 1)

        # Plotting of solid and dashed lanes
        if linesP is not None:
            # Selecting first line as solid lane
            l = linesP[0][0]
            # determining slope of solid lane
            m = (l[3] - l[1])/(l[2] - l[0])
            # Getting x-coordinates of solid lane for given y-coordinates 
            x_1s = find_x(l,m , 340)
            x_2s = find_x(l,m , height-1)

            # cv2.line(img_flip_lr, (x_1s, 340), (x_2s,height-1), (0,255,0), 3, cv2.LINE_AA)
            # Plotting solid lane as green
            cv2.line(frame , (x_1s, 340), (x_2s,height-1), (0,255,0), 3, cv2.LINE_AA)

            # Passing all the lines from hough transfrom and slope of solid lane ,to determine dashed lanes 
            m_d , linees = lane_type(linesP , m)
            # Getting x-coordinates of dashed lane for given y-coordinates 
            x_1d = find_x(linees,m_d , 340)
            x_2d = find_x(linees,m_d , height-1)
            # cv2.line(img_flip_lr, (x_1d, 340), (x_2d,height-1), (0,0,255), 3, cv2.LINE_AA)
            # Plotting dashed lane as red
            cv2.line(frame, (x_1d, 340), (x_2d,height-1), (0,0,255), 3, cv2.LINE_AA)

        # Displaying detected edge
        cv2.imshow("Edges detected", dst)

        # cv2.imshow("Detected Lines (Dashed:red & Solid:green) - Probabilistic Line Transform", img_flip_lr)  
        # Displaying classified lane
        cv2.imshow("Detected Lines (Dashed:red & Solid:green) - Probabilistic Line Transform", frame)  

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()