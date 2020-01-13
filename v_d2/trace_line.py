#from flask_opencv_streamer.streamer import Streamer
from streamer import Streamer
import cv2

streamer=Streamer(8888)
cameraID=0
VCap=cv2.VideoCapture(cameraID)
if not VCap.isOpened():
    print("ERROR! Check the camera.")
while True:
    ret, frame=VCap.read()


    ###################linetrace################
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    rc, gray = cv.threshold(image, T, 255, 0)




    streamer.update_frame(frame)

    if not streamer.is_streaming:
        streamer.start_streaming()
    cv2.waitKey(10)
