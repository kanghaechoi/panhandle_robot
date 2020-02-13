import time
import numpy as np
import math
import cv2
from streamer import Streamer
from sys import argv
import socketio

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

#maint=False
#dest=-1
sio = socketio.Client()
#address=[000,101,102,103,203,202,201]
#time_list=[1.8,2.9,2.7,3.8,2.9,2.7,3.2]
address=[000,101,102,103,203,202,201]
#time_list=[[],[1.8,2.9,2.7,3.8,2.9,2.7,3.2],[1.8,2.7,2.9,3.8,2.7,2.9,3.2]]
time_list=[[],[1.8,2.9,2.6,3.8,2.9,2.7,3.2],[1.8,3.2,2.9,2.6,3.8,2.9,2.7]]
#now=0
#old=[0,0]
#prog_time=0
#direction = 1 # 1: clockwise -1: counter

isSign=True

class Status:
    now=0
    dest=-1
    speed=[0,0]
    prog_time=0
    direction = 1 # 1: clockwise, -1: counter
    isMaint = False
    isGoing = False
    red = 0


status = Status()

@sio.event
def connect():
    print('connect established')

@sio.on('message',namespace='/robot')
def onMessage(data):
    print('received', data)
    #global dest, prog_time
    #prog_time=0
    #dest = data.split()[1]
    #if not maint:
    #    follow()
    global status
    status.prog_time = 0
    status.dest = data.split()[1]
    if not status.isMaint:
        print("go!!")
        status.isGoing=True
        follow()

@sio.on('reset', namespace='/robot')
def onReset():
    print('reset')
    global status
    status.dest = -1
    status.now = 0
    status.direction = 1
    status.speed=[0,0]
    status.progtime = 0
    status.red = 0
    status.isGoing = False

@sio.on('maintenance',namespace='/robot')
def onMaintenance(data):
    print('received Maintenance: ', data)
    global status
    if data==1:
        status.isMaint=True
    else:
        status.isMaint=False
        if status.isGoing==True:
            print("go!")
            follow()

@sio.event
def disconnect():
    print('disconnected')

def stop():
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = 0
    #TODO


def simul():
    global now, address, maint, frame
    while True:
        if maint:
            stop()
            print("maintenance mode")
            break
        time.sleep(1)
        if now==1:
            now=now+1
            print(address[now])
            if address[now]==int(dest):
                break
        elif now==2:
            now=now+1
            print(address[now])
            if address[now]==int(dest):
                break
        elif now==3:
            now=now+1
            print(address[now])
            if address[now]==int(dest):
                break
        if now==4:
            now=now+1
            print(address[now])
            if address[now]==int(dest):
                break
        elif now==5:
            now=now+1
            print(address[now])
            if address[now]==int(dest):
                break
        elif now==6:
            now=0
            print(address[now])
            if address[now]==int(dest):
                break
        elif now==0:
            now=now+1
            print(address[now])
            if address[now]==int(dest):
                break

def follow():
    i=0
    #global isSign, now, dest, maint, prog_time, streamer, direction
    global status, streamer
    width=160
    height=120
    green=0
# calculate direction
    expTime=[0,0,0]
    for t in {-1,1}:
        n=status.now
        if t!=status.direction: expTime[t]+=2
        while address[n]!=int(status.dest):
            expTime[t]+=time_list[t][n]
            n=(n+t)%len(address)
    new_direction = 1 if expTime[-1]>expTime[1] else -1
      
    if status.direction!=new_direction:
        if status.direction==1:
            kit.continuous_servo[0].throttle = -1 # CC turn
            kit.continuous_servo[1].throttle = -1
        else:
            kit.continuous_servo[0].throttle = 1 # clockwise
            kit.continuous_servo[1].throttle = 1
        status.speed = [kit.continuous_servo[0].throttle, kit.continuous_servo[1].throttle]
        time.sleep(1.2)
        while True:
            if status.isMaint:
                status.isMaint=True
                stop()
                print("maintenance mode")
                break
            frame2 = cv2.resize(frame, (width,height))
            hsv=cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
            h=height//3
            crop=hsv[height-h:height,:]
        
            lower_y = np.array([25,20,200]) # 25, 80, 80  #40 140 80
            upper_y = np.array([40,255,255]) # 40, 255, 255 #50 255 255
            mask_y=cv2.inRange(crop,lower_y,upper_y)

            if np.sum(mask_y[(4*h)//5:h,:])!=0:
                #direction=new_direction
                '''
                kit.continuous_servo[0].throttle=kit.continuous_servo[0].throttle/2
                kit.continuous_servo[1].throttle=kit.continuous_servo[1].throttle/2
                time.sleep(0.01)
                kit.continuous_servo[0].throttle=kit.continuous_servo[0].throttle/2
                kit.continuous_servo[1].throttle=kit.continuous_servo[1].throttle/2
                time.sleep(0.01)
                kit.continuous_servo[0].throttle=kit.continuous_servo[0].throttle/2
                kit.continuous_servo[1].throttle=kit.continuous_servo[1].throttle/2
                time.sleep(0.01)
                '''
                kit.continuous_servo[0].throttle = 0
                kit.continuous_servo[1].throttle = 0
                status.speed=[0,0]
                break
        status.direction=new_direction
    else:
        kit.continuous_servo[0].throttle = min(1, max(-1, status.speed[0]))
        kit.continuous_servo[1].throttle = min(1, max(-1, status.speed[1]))
    
    while True:
        start = time.perf_counter()
        frame2 = cv2.resize(frame, (width,height))
        if status.isMaint:
            status.prog_time += time.perf_counter()-start
            stop()
            print("maintenance mode")
            break
        hsv=cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        lab=cv2.cvtColor(frame2, cv2.COLOR_BGR2LAB)
        h=height//3
        crop=hsv[height-h:height,:]
        
        lower_y = np.array([25,20,160]) # 25, 20, 200
        upper_y = np.array([40,255,255]) # 40, 255, 255 #50 255 255
        mask_y=cv2.inRange(crop,lower_y,upper_y)
        obstacle=0
        streamer.update_frame(mask_y)
        if np.sum(mask_y[(4*h)//5:h,:])==0:
            status.isMaint=True
            obstacle=1
            status.prog_time += time.perf_counter()-start
            stop()
            sio.emit('maintenance', 1, namespace='/robot')
            print("obstacle")
            break

        lower_r=np.array([160,80,150]) # 160 100 150
        upper_r=np.array([180,255,255])
        #lower_g=np.array([55,80,90]) #55 90 100
        #upper_g=np.array([75,180,255]) #75 120 150
        mask_r=cv2.inRange(crop,lower_r,upper_r) 
#        mask_g=cv2.inRange(hsv, lower_g, upper_g)
#        mask_g2=cv2.inRange(lab, np.array([20,95,135]), np.array([180,115,155]))
        #mask_g=np.bitwise_and(mask_g,mask_g2)
        new_red = np.sum(mask_r)
#        new_green = np.sum(mask_g)
        if new_red>(width*h*255)/8192:
            status.red=20
        elif new_red==0:
            status.red -= 1
            if status.red==0:
                status.now=0
                status.prog_time=0
                print("STOP sign, dest: ", status.dest)
                if int(status.dest)==0 or int(status.dest)==-1:
                    status.dest=-1
                    stop()
                    print("STOP by Stop sign")
                    status.isGoing=False
                    sio.emit('message', "Arrived "+str(address[status.now]), namespace='/robot')
                    break
        M=cv2.moments(mask_y)

        #print(mask_y.shape)
        if M["m00"]==0:
            continue
        p3=[(M["m10"]/M["m00"]-width/2),(h-M["m01"]/M["m00"])]
        
        
        msg_p0 =  "p3[0] {0}".format(int(p3[0]))
        msg_p1 =  "p3[1] {0}".format(int(p3[1]))

        i=i+1
       
        pi=math.pi
        y=1
        base=6
        a=pi # px/frame
        theta=math.atan2(0.9*(p3[1]+height/30),p3[0]) # 0.9 /30 working
        if kit.continuous_servo[0].throttle<0.1 and kit.continuous_servo[1].throttle<0.1:
            start=time.perf_counter()
        if theta>=pi/2:
            theta=pi-theta
            x=(a-y*(pi-2*theta))/a
            speed=max(0.1,math.log(x,base)+1)
            #speed=max(0.1,x)
            kit.continuous_servo[0].throttle = 1*speed/2
            kit.continuous_servo[1].throttle = -1
            
        else:
            x=(a-y*(pi-2*theta))/a
            #speed=max(0.1,x)
            speed=max(0.1,math.log(x,base)+1)
            kit.continuous_servo[0].throttle = 1
            kit.continuous_servo[1].throttle = -1*speed/2
        status.speed=[kit.continuous_servo[0].throttle, kit.continuous_servo[1].throttle]
        #cv2.imwrite("./photos/out3/%d.jpg"%i,hsv)
        #cv2.imwrite("./photos/out/%d.jpg"%i,mask)
        status.prog_time += time.perf_counter()-start
        if status.prog_time>time_list[status.direction][status.now]:
            print("prog_time, arrived_time: ", status.prog_time, time_list[status.direction][status.now])
            status.now=(status.now+status.direction)%7
            status.prog_time=0
            print("now: ", address[status.now], "dest: ", status.dest)
            if address[status.now]==int(status.dest):
                status.dest=-1
                stop()
                status.isGoing = False
                sio.emit('message', "Arrived "+str(address[status.now]), namespace='/robot')
                break

if __name__ == '__main__':
    
    streamer = Streamer(8888)
    cameraID = 0
    VCap = cv2.VideoCapture(cameraID)
    if not VCap.isOpened():
        print("ERROR! Check the camera.")
        exit(0)
    if not streamer.is_streaming:
        streamer.start_streaming()
    ret, frame = VCap.read()
    streamer.update_frame(frame)
    sio.connect('http://mellon.andrew.cmu.edu:9999', namespaces=['/robot'])
    try:
        while True:
            if not streamer.is_streaming:
                streamer.start_streaming()
            ret, frame = VCap.read()
            #streamer.update_frame(frame)
    except Exception as e:
        print(e)
        kit.continuous_servo[0].throttle = 0
        kit.continuous_servo[1].throttle = 0
        exit(0)