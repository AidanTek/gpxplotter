from time import sleep
from random import randint

stepres = 1

print('Working out some random numbers')
sleep(1)

maxx = randint(0,30)-15
minx = randint(0,30)-15
while minx >= maxx:
	minx = randint(0,30)-15

maxy = randint(0,30)-15
miny = randint(0,30)-15
while miny >= maxy:
	miny = randint(0,30)-15

dimx = 4000
dimy = 1500

distx = maxx-minx
disty = maxy-miny

print('Results:')
sleep(1)
print('maxx = {}, minx = {}, dimx = {}, maxy = {}, miny = {}, dimy = {}'.format(maxx,minx,distx,maxy,miny,disty))
sleep(2)

print('Working out safe resolution')
sleep(1)

if distx > disty:
	print('X dimension is greater range')
	sleep(1)
	stepres = distx / dimx
	print('stepres for x is {}'.format(stepres))
	sleep(1)

	if disty / stepres > dimy:
		print('This is not compatible with y')
		sleep(1)
		print('Repairing')
		while (disty / stepres) > dimy:
			stepres = stepres*1.05
			print(stepres)
		print('Done!')
		sleep(1)
		print('stepres ammended to {}'.format(stepres))
		sleep(1)

	else:
		print('Everything is fine')
		sleep(1)
else:
	print('Y dimension is greater range')
	sleep(1)
	stepres = disty / dimy
	print('stepres for y is {}'.format(stepres))
	sleep(1)

	if distx / stepres > dimx:
		print('This is not compatible with x')
		sleep(1)
		print('Repairing')
		while (distx / stepres) > dimx:
			stepres = stepres*1.05
			print(stepres)
		print('Done!')
		sleep(1)
		print('stepres ammended to {}'.format(stepres))
		sleep(1)
	else:
		print('Everything is fine')
		sleep(1)

plotx = distx/stepres
ploty = disty/stepres

print('X greatest plot = {}, Y greatest plot = {}'.format(plotx, ploty))
sleep(5)
