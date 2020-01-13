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
    streamer.update_frame(frame)

    if not streamer.is_streaming:
        streamer.start_streaming()
    cv2.waitKey(10)
