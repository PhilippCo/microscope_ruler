import numpy as np
import cv2

 
point    = (0,0)
mode     = 0
startp   = (0,0)
scale    = 0.010019537105994292
measured = 0


def distance(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return (dx**2 + dy**2)**0.5


def click(event, x,y, flags, param):
    global point, mode, startp, scale, measured
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pressed", x,y)
        point = (int(x/2),int(y/2))

        if mode == 0: #select 1. point to measure
            startp = point
            mode = 1

        elif mode == 1: #select 2. point to measure
            measured = distance(startp, point) * scale
            print("Distance: {0:0.3f}mm".format(measured))
            mode = 0

        elif mode == 3: #select 1. point to calibrate
            startp = point
            mode = 4

        elif mode == 4: #select 2. point to calibrate
            real_distance = float(input("Distance in mm: ")) #real distance
            print("calibration done")
            measured_distance = distance(startp, point)
            scale = real_distance / measured_distance
            measured = measured_distance * scale
            print("Distance: {0:0.3f}mm".format(measured))
            print("Scale: {0:0.4f} mm/pixel".format(scale))
            mode = 0 #calibration done

            
         

title = "Microscope Ruler -- q:quit c:calibrate"
cv2.namedWindow(title)
cv2.setMouseCallback(title, click)

 
cap = cv2.VideoCapture(2) #select camera here <-

while (True):
     
    stream = cv2.waitKey(1)
    ret,frame = cap.read()

    cv2.line(frame, startp, point, (0, 0, 255), thickness=3)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (10, 30)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    image = cv2.putText(frame, "{0:0.2f}mm".format(measured), org, font, 
                   fontScale, color, thickness, cv2.LINE_AA)

    frame = cv2.resize(frame, (0,0), fx=2, fy=2)
    cv2.imshow(title, frame)
     
    if stream & 0XFF == ord('q'):  #quit
        break

    if stream & 0XFF == ord('c'):
        print("Start calibration")
        print("Click on first point")
        mode = 3

         
cap.release()
cv2.destroyAllWindows()