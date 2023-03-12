# importing libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video/problem3.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video file")

# Function for determining radius of curvature
def radius_cur(A , B , y):
    X = np.power(2*A*y + B , 2)
    Nr = np.power(1+X , 1.5)
    Dr = np.abs(2*A)
    return (Nr/Dr)

# Function to get points on the curve
def get_curve_points( curve , height ,result , detected_lanes) :
    lspace = np.linspace(0 , height , 20)
    draw_y = lspace
    draw_y_int = [int(x) for x in draw_y]
    draw_x = np.polyval(curve, draw_y)  
    draw_x_int = [int(x) for x in draw_x]
    # Plotting detected points
    for i in range(len(draw_x_int)-1):
        if detected_lanes[draw_y_int[i]][draw_x_int[i]] :
            cv2.circle(result,  (draw_x_int[i] , draw_y_int[i]), 5, (255, 0 , 0), 2)
    # Needs to be int32 and transposed
    return (np.asarray([draw_x, draw_y]).T).astype(np.int32)   

# To detect turn
def detect_turn(A_solid ,A_dashed) :
    if (A_solid + A_dashed)/2 > 0:
        return "TURN RIGHT"
    elif (A_solid + A_dashed)/2 < 0:
        return "TURN LEFT"
    else :
        return "GO STRAIGHT"

# To resize frame
def resize(frame , x , y):
    dimensions = ( int(frame.shape[1]*x) , int(frame.shape[0]*y))
    return cv2.resize(frame, dimensions , interpolation = cv2.INTER_AREA)

# Read until video is completed
while(cap.isOpened()):
	
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        first = frame.copy()
        second = frame.copy()
    # Blank white image
        white_blankimage = 255 * np.ones(shape=[100, 1780, 3], dtype=np.uint8)
    # Points on image frame to perform homography
        pts1 = np.float32([[585, 450], [165, 705], [1180, 705] ,[750, 450]])
    # Final destination points (New frame coordinates)
        pts2 = np.float32([[0, 0], [0, 600],[500, 600] ,[500, 0]])
     
    # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # Frame with top-view of road
        result = cv2.warpPerspective(frame, matrix, (500, 600))   

        polynomialgon = result.copy()
    # Plotting region of homography onto the frame
        cv2.line(second , (585, 450), (165, 705), (0,255,0), 3, cv2.LINE_AA) 
        cv2.line(second , (165, 705), (1180, 705), (0,255,0), 3, cv2.LINE_AA)
        cv2.line(second , (1180, 705), (750, 450), (0,255,0), 3, cv2.LINE_AA)
        cv2.line(second , (750, 450), (585, 450), (0,255,0), 3, cv2.LINE_AA)

    ############# YELLOW lane detection ###############
    # Applying blur to remove noises from top-view frame
        gaus = cv2.GaussianBlur(result,(9,9),cv2.BORDER_DEFAULT)          
    # Converting into hsv color format for lane detection
        hsv = cv2.cvtColor(gaus, cv2.COLOR_BGR2HSV)
    # Applying limits for yellow color 
        low_yellow = np.array([10, 100, 160])
        high_yellow = np.array([35, 255, 255])
    # Creating mask       
        mask = cv2.inRange(hsv, low_yellow, high_yellow)
    # Getting frame with yellow lane using bitwise operation
        yellow_lane = cv2.bitwise_and(result,result, mask= mask)
        gray1 = cv2.cvtColor(yellow_lane,cv2.COLOR_BGR2GRAY)
        threshold1, thresh1 = cv2.threshold(gray1, 150, 255, cv2.THRESH_BINARY)

    # Storing pixels with yellow color 
        Y_s, X_s = np.where(np.all(yellow_lane!=[0],axis=2))
    # 2nd degree polynomial in the form 'x = A*y^2 + B*y + C'
        curve_solid = np.polyfit(Y_s , X_s , 2)
    # Calculating radius of curvature for solid lane
        radius_solid  = radius_cur(curve_solid[0] , curve_solid[1] , yellow_lane.shape[0])
        A_solid = curve_solid[0]
        print("radius solid lane : "+str(radius_solid))
 
    ############ WHITE lane detection #################
    # Converting top-view into grayscale
        gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    # Applying threshhold for white lane
        threshold, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    # Plotting both yellow and white lane together
        detected_lanes = cv2.bitwise_or(thresh1 , thresh , mask = None)
 
    # Storing pixels with white color 
        Y_d , X_d = np.where(thresh==255 )
    # Curve for dashed lane
        curve_dashed = np.polyfit(Y_d , X_d , 2)
        radius_dashed = radius_cur(curve_dashed[0] , curve_dashed[1] , result.shape[0])
        print("radius dashed lane : "+str(radius_dashed))

        A_dashed = curve_dashed[0]
    # Getting solid curve points   
        draw_points_solid = get_curve_points(curve_solid , result.shape[0] , result , detected_lanes)     
    # Getting dashed curve points  
        draw_points_dashed = get_curve_points(curve_dashed , result.shape[0] , result , detected_lanes) 
    # Plotting curve equations
        cv2.polylines(result, [draw_points_solid], False, (0,0,0) ,4)  
        cv2.polylines(result, [draw_points_dashed], False, (0,0,0) ,4)  

    # Plotting colored region formed by the curves on top-view image          
        points2 = np.flipud(draw_points_dashed)
        points = np.concatenate((draw_points_solid, points2))
        cv2.fillPoly(polynomialgon, [points], color=[255,0,0])

    # Converting top-view to original form
        matrix_inv = cv2.getPerspectiveTransform(pts2, pts1)
        original_view = cv2.warpPerspective(polynomialgon, matrix_inv, (frame.shape[1], frame.shape[0])  )         

        answer = (radius_solid+radius_dashed)/2 
    # Getting final output image
        final_output = cv2.bitwise_or(original_view , frame , mask = None)

        cv2.putText(final_output , detect_turn(A_solid ,A_dashed) , (10,50) , cv2.FONT_HERSHEY_TRIPLEX ,
                     1.0 , (0,0,255) ,3)
    
    # Resizing and merging frames
        first_resize = resize(first , 25/128 , 0.2)
        second_resize = resize(second , 25/128 , 0.2)
        H1 = np.concatenate((first_resize, second_resize), axis=1)

        detected_lanes_3 = cv2.cvtColor(detected_lanes , cv2.COLOR_GRAY2BGR) 
        third_resize = resize(detected_lanes_3 , 0.5 , 0.96)
        fourth_resize = resize(result , 0.5 , 0.96)
        H2 = np.concatenate((third_resize, fourth_resize), axis=1)

        V1 = np.concatenate((H1, H2), axis=0)

        H3 = np.concatenate((final_output, V1), axis=1)

        V2 = np.concatenate((H3, white_blankimage), axis=0)

        cv2.putText(V2 , '(1)' , (1308,25) , cv2.FONT_HERSHEY_TRIPLEX , 0.7 , (0,0,255) ,2)

        cv2.putText(V2 , '(2)' , (1563,25) , cv2.FONT_HERSHEY_TRIPLEX , 0.7 , (0,0,255) ,2)

        cv2.putText(V2 , '(3)' , (1308,187) , cv2.FONT_HERSHEY_TRIPLEX , 0.7 , (0,0,255) ,2)

        cv2.putText(V2 , '(4)' , (1563,187) , cv2.FONT_HERSHEY_TRIPLEX , 0.7 , (0,0,255) ,2)      

        cv2.putText(V2 , '(1) : Camera Feed' + ' , ' + '(2) : Selected region for homography'
                    + ' , ' + '(3) : After Homography and detecting lanes' + ' , ' + 
                    ' (4) : Detected curve and points'  , (40,750) , cv2.QT_FONT_NORMAL ,
                     0.7 , (0,0,0) ,2)  

        cv2.putText(V2 , 'Radius of curvature : '+ str(answer) + '(m)' , (40,800) , cv2.QT_FONT_NORMAL ,
                     0.7 , (0,0,0) ,2)             
        cv2.imshow("Final Result" ,V2)

        print("Frame done")

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
