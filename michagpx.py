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
import csv
from time import sleep
from stepperdrive import reposxy

# These objects are 'global' parameters used by the script
minx = 0
miny = 0
stepres = 0

gridx = 7000
gridy = 3000

fp = '/home/pi/my_files/It_might_not_be_there_an_exhibition_tour/'
route = 'track_points.csv' # this could become a tuple to handle multiple files

# A function to figure out the maximum plotter dimensions needed for a loaded route
# Currently this is using a fixed file and will need to be updated to take multiple possibilities
# Currently I am imagining that we have a plot 'resolution' of 1000*1000
def scaledimensions():
    global minx, miny, fp, csvfile, stepres, gridx, gridy

    # Local parameters required for function
    maxx = 0
    minx = 999
    maxy = 0
    miny = 999

    with open(fp+route, newline='') as csvfile:
        coor = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in coor:
            try:
                x = float(row[0])
                if x >= maxx:
                    maxx = x
                elif x <= minx:
                    minx = x
            # The first line of the .csv file will cause a ValueError (nan)
            except ValueError:
                pass

            try:
                y = float(row[1])
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
        if xdistance > ydistance:
            print('X dimension has biggest difference')
            stepres = (xdistance/gridy)
        else:
            print('Y dimension has biggest difference')
            stepres = (ydistance/gridx)

        print('Step resolution = {}'.format(stepres))

        csvfile.close()

# This function is the main plot sequence
def plot():
    global stepres

    with open(fp+route, newline='') as csvfile:
        coor = csv.reader(csvfile, delimiter=',', quotechar='|')

        # Local parameters required for function
        x = 0
        y = 0
        xpos = 0
        ypos = 0
        stepx = 0
        stepy = 0
        dirx = 0
        diry = 0
        nextx = 0
        nexty = 0

        # Increment the steppers:
        for row in coor:
            try:
                x = float(row[0])
                xpos = int((x-minx)/stepres)
            # The first line of the .csv file will cause a ValueError (nan)
            except ValueError:
                pass

            if not xpos == stepx:
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
                y = float(row[1])
                ypos = int((y-miny)/stepres)
            # The first line of the .csv file will cause a ValueError (nan)
            except ValueError:
                pass

            if not ypos == stepy:
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
        reposxy(stepx, stepy, 0, 0, 0.002)


# Main script is below this line:
print('Checking maximum dimensions of file:')

scaledimensions()

print('Starting plot...')
sleep(3)
plot()
print('Done!')

'''
Math:

onestep = (maxx-minx)/plotterresolution (this doesn't account for a safe margin)
stepposition = (dimension-mindimension)/onestep

'''
