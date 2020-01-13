# File: server.py
#
# Author: Anthony J. Lattanze, Aug 2019
#
# Description:
# 
# This program is 1 of 3 programs intended to demonstrate how sockets work between three
# programs: a client, middleware, and a server. This program is the server. Start this 
# program first. It will display the hostname and IP address in case you need them for 
# the middleware program to communicate with the server.

import socket
from sys import argv
from adafruit_servokit import ServoKit

# Get the hostname and IP address of this machine and display it.
host_name = socket.gethostname()

try:
    host_ip = socket.gethostbyname(socket.gethostname())
    # On many linux systems, this always gives 127.0.0.1. Hence...
except:
    host_ip = ''
if not host_ip or host_ip.startswith('127.'):
    # Now we get the address the hard way.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('4.2.2.1', 0))
    host_ip = s.getsockname()[0]

port=7777
if len(argv)>1:
    port=int(argv[1])

print("Server Hostname:: ",host_name) 
print("Server IP:: ",host_ip, " port: ",port)

# Set up message that will be sent back to the middleware, then
# get a socket. We bind to the local host on port 8080. We can
# accept up to 5 simultainious connections.

msg = "Msg received by the server..."
servconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servconn.bind((host_ip, port))
servconn.listen(5)

# Here we loop forever to manage connections.
kit = ServoKit(channels=16)
while True:
    # When the middleware requests a connection it is
    # accepted in the following statement. 
    # Here we connect and receive upto 4096 bytes of data and
    # then print it out.
    mwconn, addr = servconn.accept()
    print("connected")
    mwdata = mwconn.recv(16).decode()
    print("Middleware::", mwdata)
    key, pressed=mwdata.split()
    print(key)
    if pressed=='u':
        kit.continuous_servo[0].throttle = 0
        kit.continuous_servo[1].throttle = 0
    else:
        if key == 'o':
            kit.servo[0].angle=45
        if key =='x':
            kit.continuous_servo[0].throttle = 0
            kit.continuous_servo[1].throttle = 0
        if key == 'w':
            kit.continuous_servo[0].throttle = 1
            kit.continuous_servo[1].throttle = -1
        if key == 's':
            kit.continuous_servo[0].throttle = -1
            kit.continuous_servo[1].throttle = 1
        if key == 'd':
            kit.continuous_servo[0].throttle = 0.5
            kit.continuous_servo[1].throttle = 0.5
        if key == 'a':
            kit.continuous_servo[0].throttle = -0.5
            kit.continuous_servo[1].throttle = -0.5

    # Now we send a response back to middleware
    # mwconn.send(msg.encode('ascii'))
    mwconn.close()
    print("Middleware client disconnected")
                                    