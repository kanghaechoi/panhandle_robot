# File: servodem.py
#
# Author: Anthony J. Lattanze, Aug 2019
#
# Description:
# 
# This program is demonstrates how to use the Adafruit PWM hat and library
# to control servos on the PI bots.

# We need the time library so we can sleep
import time

# First we pick up the servokit library
from adafruit_servokit import ServoKit

# Now we instantiate a library - note there are 16 channels on the PWM
# hat. We only use channels 0 and 1 for the bot's servos.
kit = ServoKit(channels=16)

# The servos on the bot are obviously continuous servos, so we use the
# continous_servo methods. We control the servos velocity and direction
# using the throttle command. A throttle value of one will move the
# servo in a direction at full speed. A throttle value of minus one will 
# move the servo in the opposite direction at full speed. This is shown
# below. Note that both servos will move in the same direction in this 
# example because they are physically opposite of one another.   

kit.continuous_servo[0].throttle = 1
kit.continuous_servo[1].throttle = -1

# Now we pause for 5 seconds, but note that the servos keep going. That
# is becase servo control is asyncronous.

time.sleep(5)

# Note that fractional values between zero and one can also be used, but
# the resolution is not very granular. Here they flip directions and go
# half speed

kit.continuous_servo[0].throttle = -0.5
kit.continuous_servo[1].throttle = 0.5
time.sleep(5)

# Couple more checks...

kit.continuous_servo[0].throttle = 1
kit.continuous_servo[1].throttle = 1
time.sleep(5)

kit.continuous_servo[0].throttle = -0.5
kit.continuous_servo[1].throttle = -0.5
time.sleep(5)

# Stop the servos. Please note, that if the servos do not full stop when you 
# zero them, then you should notify the course instructor so he can 
# calibrate them. This only takes a few minutes.

kit.continuous_servo[0].throttle = 0
kit.continuous_servo[1].throttle = 0