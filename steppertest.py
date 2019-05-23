import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

stepPin = 17
dirPin = 27

stepspeed = 0.005

GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

GPIO.output(dirPin, GPIO.HIGH)
for i in range(800):
    GPIO.output(stepPin, GPIO.HIGH)
    time.sleep(stepspeed)
    GPIO.output(stepPin, GPIO.LOW)
    time.sleep(stepspeed)

GPIO.output(dirPin, GPIO.LOW)
for i in range(800):
    GPIO.output(stepPin, GPIO.HIGH)
    time.sleep(stepspeed)
    GPIO.output(stepPin, GPIO.LOW)
    time.sleep(stepspeed)
