import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

stepxpin = 17
dirxpin = 27

stepypin = 23
dirypin = 24

GPIO.setup(stepxpin, GPIO.OUT)
GPIO.setup(dirxpin, GPIO.OUT)
GPIO.setup(stepypin, GPIO.OUT)
GPIO.setup(dirypin, GPIO.OUT)

# This is a function to move both steppers simultaneously
# Example Usage (move x 300 forwards and y 120 backwards:
# reposxy(300, 120, 1, 0)

def reposxy(stepx, stepy, dirx, diry, stepspeed):
    # Set direction of X
    if dirx == 1:
        GPIO.output(dirxpin, GPIO.HIGH)
    else:
        GPIO.output(dirxpin, GPIO.LOW)

    # Set direction of Y
    if diry == 1:
        GPIO.output(dirypin, GPIO.HIGH)
    else:
        GPIO.output(dirypin, GPIO.LOW)

    # Determine which movement is greater, x or y:
    # Then move the two steppers at a ratio to each other, for better angles
    if stepx - stepy > 0:
        try:
            ratio = int(stepx/stepy)
            for n in range(stepx):
                GPIO.output(stepxpin, GPIO.LOW)
                GPIO.output(stepypin, GPIO.LOW)
                time.sleep(stepspeed)
                GPIO.output(stepxpin, GPIO.HIGH)
                if n % ratio == 0:
                    GPIO.output(stepypin, GPIO.HIGH)
                time.sleep(stepspeed)
        
        except ZeroDivisionError: 
            for n in range(stepx):
                GPIO.output(stepxpin, GPIO.LOW)
                time.sleep(stepspeed)
                GPIO.output(stepxpin, GPIO.HIGH)
                time.sleep(stepspeed)
                
    else:
        try:
            ratio = int(stepy/stepx)
            for n in range(stepy):
                GPIO.output(stepxpin, GPIO.LOW)
                GPIO.output(stepypin, GPIO.LOW)
                time.sleep(stepspeed)
                GPIO.output(stepypin, GPIO.HIGH)
                if n % ratio == 0:
                    GPIO.output(stepxpin, GPIO.HIGH)
                time.sleep(stepspeed)
        
        except ZeroDivisionError:
            for n in range(stepy):
                GPIO.output(stepypin, GPIO.LOW)
                time.sleep(stepspeed)
                GPIO.output(stepypin, GPIO.HIGH)
                time.sleep(stepspeed)



    


