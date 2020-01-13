"""
https://github.com/oitsjustjose/Flask-OpenCV-Streamer
"""

"""Stores a Streamer class"""
import time
from threading import Thread

import cv2
from flask import Flask, Response, render_template, request
from flask_socketio import SocketIO

frame=None
frame_rate=0
port=8888
app = None
socketio=None
is_streaming = False
VCap=None
server=None

def start_streaming():
    @app.route("/video_feed")
    def video_feed():
        """Route which renders solely the video"""
        return Response(
            gen(), mimetype="multipart/x-mixed-replace; boundary=jpgboundary"
        )

    @app.route("/")
    def index():
        """Route which renders the video within an HTML template"""
        return render_template("index.html")

    @socketio.on('connect')
    def on_connect():
        print('connected!')

    @socketio.on('button')
    def on_button(data):
        print('received')
        print(data)

    @socketio.on('connection')
    def on_connection(data):
        print('hi')

    thread = Thread(
        daemon=True,
        target=socketio.run,
        kwargs={
            "app": app,
            "host": "0.0.0.0",
            "port": port,
            "debug": False,
            "threaded": True,
        },
    )
    thread.start()
    is_streaming = True


def get_frame(frame):
    """Encodes the OpenCV image"""
    _, jpeg = cv2.imencode(
        ".jpg",
        frame,
        params=(cv2.IMWRITE_JPEG_QUALITY, 70),
    )
    return jpeg.tobytes()

def gen():
    """A generator for the image."""
    header = "--jpgboundary\r\nContent-Type: image/jpeg\r\n"
    prefix = ""
    while True:
        #ret, frame =VCap.read()
        stream=frame
        msg = (
            prefix
            + header
            + "Content-Length: {}\r\n\r\n".format(len(stream))
        )

        yield (msg.encode("utf-8") + stream)
        prefix = "\r\n"
        time.sleep(1 / (10*frame_rate))



if __name__=='__main__':
    port = 8888
    frame_rate = 30
    server=0
    app=Flask(__name__)
    socketio=SocketIO(app)
    VCap=cv2.VideoCapture(server)
    if not VCap.isOpened():
        print("ERROR! Check the camera.")
        exit(0)

    start_streaming()
    while True:
        if not is_streaming:
            start_streaming()
        ret, f = VCap.read()
        frame = get_frame(f)
        cv2.waitKey(10)


#    socketio.run(app,host="0.0.0.0", port=8888, debug=True)
