'''
GPS mapped route plotter

This script is for the Raspberry Pi. It takes data collected from a GPS (currently in .csv format) and converts it to a 2d plot for a pair of steppers to follow

Michaela Davidova and Aidan Taylor. Cardiff Metropolitan University. 2019

ToDo:
* Use raw .gpx file without conversion - I spotted a github repo that might do this
* Add stepper return to zero position function
* Adjust stepper speed according to route speed
* Add basic GPIO input control to start plotter
* Activate LED at start of plot
* Add GPIO for stepper control and write stepper functions
* Translate stepper resolution, make gears?
* Add servo control
* Add some way to choose different between different routes

'''

# import required libraries:
import gpxpy
from time import sleep
from stepperdrive import reposxy
import RPi.GPIO as GPIO
from random import randint

# Hardware Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# led
ledpin = 21
GPIO.setup(ledpin, GPIO.OUT)

# switches
xswitch = 12
yswitch = 16
GPIO.setup(xswitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yswitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

xstate = 1
ystate = 1
lastxstate = 1
lastystate = 1
debounce = 0.01

# These objects are 'global' parameters used by the script
minx = 0
miny = 0
stepres = 0

gridx = 4000
gridy = 2700

#random file object
randfile = randint(1,13)

fp = '/home/pi/my_files/gpx/'
route = '3.gpx' # this could become a tuple to handle multiple files
#route = '{}.gpx'.format(randfile)

print('This route is {}'.format(route))

# A function to figure out the maximum plotter dimensions needed for a loaded route
# Currently this is using a fixed file and will need to be updated to take multiple possibilities
# Currently I am imagining that we have a plot 'resolution' of 1000*1000
def scaledimensions():
    global minx, miny, fp, csvfile, stepres, gridx, gridy

    # Local parameters required for function
    maxx = -999
    minx = 999
    maxy = -999
    miny = 999

    gpx_file = open(fp+route, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.time))
                try:
                    x = float(point.longitude)
                    if x >= maxx:
                        maxx = x
                    elif x <= minx:
                        minx = x
                # The first line of the .csv file will cause a ValueError (nan)
                except ValueError:
                    pass

                try:
                    y = float(point.latitude)
                    if y >= maxy:
                        maxy = y
                    elif y <= miny:
                        miny = y
                # The first line of the .csv file will cause a ValueError (nan)
                except ValueError:
                    pass

        # Uncomment the next line to print out all the coordinates:
        # print(', '.join(row)) # This specifically prints column 0 from the .csv file

        print()
        print('Max X = {}, Min X = {}, Max Y = {}, Min Y = {}'.format(maxx, minx, maxy, miny))

        xdistance = (maxx - minx)
        ydistance = (maxy - miny)

        # check whether x or y has greatest min/max difference - this will be used to set scale:
        print('Route distance X = {}, Route distance Y = {}'.format(xdistance, ydistance))
        if xdistance < ydistance:
            print('X dimension has smallest difference')
            stepres = (xdistance/gridx)
            #check maximum dimensions of opposite axis:
            print('Max Y = {}'.format(maxy/stepres))
        else:
            print('Y dimension has smallest difference')
            stepres = (ydistance/gridy)
            print('Max X = {}'.format(xdistance*stepres))

        print('Step resolution = {}'.format(stepres))

        gpx_file.close()

# This function is the main plot sequence
def plot():
    global stepres, xstate, lastxstate, ystate, lastystate

    # First return the steppers to zero position
    zerox = False
    zeroy = False

    print("Zeroing X")
    while not zerox:
        reposxy(0, 1, 1, 0, 0.002)
        xstate = GPIO.input(xswitch)
        if xstate != lastxstate:
            if xstate == 0:
                zerox = True
            lastxstate = xstate

    print("X Zero'd")
    sleep(0.5)

    print("Zeroing Y")
    while not zeroy:
        reposxy(1, 0, 0, 1, 0.002)
        ystate = GPIO.input(yswitch)
        if ystate != lastystate:
            if ystate == 0:
                zeroy = True
            lastystate = ystate

    print("Y Zero'd")
    sleep(0.5)


    #position motors at the edge of paper
    reposxy(1000,50,1,1,0.01)

    #start plot from here
    print('Starting plot...')
    sleep(0.5)

    gpx_file = open(fp+route, 'r')
    gpx = gpxpy.parse(gpx_file)

    # Local parameters required for function
    x = 0 # Raw output from file
    y = 0 # Raw output from file
    xpos = 0 # Converted output, next position
    ypos = 0 # Converted output, next position
    stepx = 0 # Current position
    stepy = 0
    dirx = 0
    diry = 0
    nextx = 0 # steps to next position
    nexty = 0

    # Increment the steppers:
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.time))
                try:
                    x = float(point.longitude)
                    xpos = int((x-minx)/stepres)
                # The first line of the .csv file will cause a ValueError (nan)
                except ValueError:
                    pass

                if not xpos == stepx:
                    if xpos < 0 or xpos > gridx:
                        nextx = 0
                    else:
                        if stepx != 0:
                            GPIO.output(ledpin, GPIO.HIGH)
                            if stepx < xpos:
                                dirx = 1
                                nextx = xpos - stepx
                            else:
                                dirx = 0
                                nextx = stepx - xpos
                else:
                    nextx = 0

                stepx = xpos

                try:
                    y = float(point.latitude)
                    ypos = int((y-miny)/stepres)
                # The first line of the .csv file will cause a ValueError (nan)
                except ValueError:
                    pass

                if not ypos == stepy:
                    if ypos < 0 or ypos > gridy:
                        nexty = 0
                    else:
                        if stepy < ypos:
                            diry = 1
                            nexty = ypos - stepy
                        else:
                            diry = 0
                            nexty = stepy - ypos
                else:
                    nexty = 0

                stepy = ypos

                print('X Actual {} || Y Actual {} || X grid {} || Y grid {} || X Steps {} || Y Steps {}'.format(x,y,xpos,ypos, nextx, nexty))

                reposxy(nextx, nexty, dirx, diry, 0.002)

    # Return to zero
    GPIO.output(ledpin, GPIO.LOW)
    reposxy(stepx, stepy, 0, 0, 0.002)


# Main script is below this line:
print('Checking maximum dimensions of file:')

scaledimensions()

sleep(3)
plot()
print('Done!')

'''
Math:

onestep = (maxx-minx)/plotterresolution (this doesn't account for a safe margin)
stepposition = (dimension-mindimension)/onestep

'''
