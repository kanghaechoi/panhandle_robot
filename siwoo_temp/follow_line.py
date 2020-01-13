import tanq_rest as tanq
import track_cv as track
import time
import numpy as np
import traceback
import math
import track_conf as tconf
import logging
import pdb
import cv2
from streamer import Streamer

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
#speed =0.2

def fwd_on():
    kit.continuous_servo[0].throttle = 1
    kit.continuous_servo[1].throttle = -1

def fwd_off():
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = 0

def back_on():
    kit.continuous_servo[0].throttle = -1
    kit.continuous_servo[1].throttle = 1

def back_off():
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = 0


def right_on(a, speed):
    #speed = abs(shift)/100
    kit.continuous_servo[0].throttle = speed
    kit.continuous_servo[1].throttle = -np.sin(a)*speed

def left_on(a, speed):
    #speed = abs(shift)/100
    kit.continuous_servo[0].throttle = np.sin(a)*speed
    kit.continuous_servo[1].throttle = -speed

def set_motors(mode):
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = 0
    # return tanq_post("/motor/" + mode)




#logging.basicConfig(filename="track.log", level=logging.DEBUG)

PN = 0

#didir= "photos/out/0.jpg"
def find_line(side,image):
    #logging.debug(("Finding line", side))
    if side == 0:
        return None, None

    for i in range(0, tconf.find_turn_attempts):
        turn(side, tconf.find_turn_step)
        angle, shift, outframe = get_vector(image)
        # angle, shift = get_vector()

        if angle is not None:
            return angle, shift, outframe

    return None, None, None


# def get_photo():
#     global PN
#     ph, hc = tanq.photo()
#     if ph is None:
#         return False, None, None
#     if not ph["rc"]:
#         return False, None, None
#     phid = ph["name"]
#     fname = tanq.get_photo(phid, "photos")
#     PN += 1
#     return True, phid, fname

# def get_vector():
def get_vector(image):

    # rc, phid, fname = get_photo()
    angle, shift, outframe = track.handle_pic(image, fout="photos/out/0_.jpg".format(PN))
    # angle, shift = track.handle_pic(fname, fout="photos/out/{0}.jpg".format(PN))
    return angle, shift, outframe


def turn(r, t):
    turn_cmd = "s0" if r > 0 else "0s"
    ret_cmd = "f0" if r > 0 else "0f"
    turn = "Right" if r > 0 else "Left"
    #logging.debug(("Turn", turn, t))
    
    #fwd_on()
    #time.sleep(t)
    #fwd_off()
    #pdb.set_trace()
    if r > 0:
        right_on()
        time.sleep(t)
    else:
        left_on()
        time.sleep(t)
    #pdb.set_trace()
    # tanq.set_motors(turn_cmd)
    # time.sleep(t)
    # tanq.set_motors(ret_cmd)


def turn_d(r, t, a, shift):
    if r > 0:
        right_on(a, t)
        #time.sleep(t)
        #time.sleep(abs(shift)/600)

    else:
        left_on(a, t)
        #time.sleep(t)
        #time.sleep(abs(shift)/600)

def check_shift_turn(angle, shift):
    turn_state = 0
    if angle < tconf.turn_angle or angle > 180 - tconf.turn_angle:
        turn_state = np.sign(90 - angle)

    shift_state = 0
    if abs(shift) > tconf.shift_max:
        shift_state = np.sign(shift)
    return turn_state, shift_state


def get_turn(turn_state, shift_state,a , shift):
    turn_dir = 0
    turn_val = 0
    if shift_state != 0:
        turn_dir = shift_state
        #turn_val = tconf.shift_step if shift_state != turn_state else tconf.turn_step
        turn_val =abs(shift)/100 if shift_state != turn_state else abs(a/180)
    elif turn_state != 0:
        turn_dir = turn_state
        turn_val = abs(a/180)
        #turn_val = tconf.turn_step
    return turn_dir, turn_val


def follow(iterations):
    i=0

    try:
        last_turn = 0
        last_angle = 0

        streamer = Streamer(8888)
        cameraID = 0
        VCap = cv2.VideoCapture(cameraID)
        if not VCap.isOpened():
            print("ERROR! Check the camera.")
            exit(0)
        while True:
            start = time.time()
            last_turn = 0
            last_angle = 0
            ret, frame = VCap.read()
            #if not cv2.imwrite("./photos/%d.jpg"%i,frame):
            #    print("can't write an image!")
            #pdb.set_trace()

            angle, shift, outframe = get_vector(frame)
            print(i, angle, shift)
            i=i+1
           
            if angle is None or 0:
                fwd_off()
                continue
            
            y=500
            a=1000 # px/frame
            h=240
            pi=math.pi
            angle=angle*pi/180
            
            theta=-math.atan(h*math.tan(angle)/(h+shift*math.tan(angle)))
            if theta>=pi/2:
                theta=pi-theta
                x=(a-y*(pi-2*theta))/a
            else:
                x=(a-y*(pi-2*theta))/a
            print(i, " Angle ", angle, " Shift ", shift, " Theta ", theta, " X ", x)
            #print("    turn_state ", turn_state, "shift_state ", shift_state, "turn_val ", turn_val)
            #pdb.set_trace()
            #outframe = cv2.imread("./photos/out/%d_.jpg"%i)
            cv2.imwrite("./photos/out/0.jpg",outframe)
            #pdb.set_trace()
            print("time : ",time.time()-start)
    except:
        print("except!")

if __name__ == '__main__':
    follow(tconf.max_steps)