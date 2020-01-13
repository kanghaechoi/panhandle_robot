import numpy as np
import cv2
import imutils
from imutils import contours
import pdb
#from imutils.perspective import four_point_transform
from streamer import Streamer


streamer = Streamer(8888)
cameraID = 0
VCap = cv2.VideoCapture(cameraID)
if not VCap.isOpened():
    print("ERROR! Check the camera.")
# while True:

ret, frame = VCap.read()
cv2.imwrite("stop.jpg",frame)

class CoordinateStore:
    def __init__(self):
        self.points = []

    def select_point(self,event,x,y,flags,param):
            if event == cv2.EVENT_LBUTTONDBLCLK:
                cv2.circle(img,(x,y),3,(255,0,0),-1)
                self.points.append((x,y))


#instantiate class
coordinateStore1 = CoordinateStore()


# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',coordinateStore1.select_point)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()


print ("Selected Coordinates: ")
for i in coordinateStore1.points:
    print (i )







w_im, h_im, _ = frame.shape
# a,b = 50,60
# [R,G, B] =[np.mean(frame[a:b,a:b,0]),np.mean(frame[a:b,a:b,1]),np.mean(frame[a:b,a:b,2])]
# print("Loc: %d, %d    RGB: %f, %f, %f"%(a, b, R,G,B))
#
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
# [L,LA, LB] =[np.mean(frame[a:b,a:b,0]),np.mean(frame[a:b,a:b,1]),np.mean(frame[a:b,a:b,2])]
# print("Loc: %d, %d    LAB: %f, %f, %f"%(a, b, L,LA, LB))
#


