#!/usr/bin/python

#Import important libraries
import serial, time, sys

#Initialize Arduino interface
ser = None
print "You are now running " + sys.argv[0]
for i in range(10):
    print "Trying to connect to /dev/ttyACM{0}".format(i)
    try:
        ser = serial.Serial('/dev/ttyACM{0}'.format(i), 38400)
    except Exception as e: pass
    else:
        print "Connected!"
        break

#Initialize a helper function
pointList = []
def write(text):
    global ser
    ser.write(bytes(text.encode('ascii')))
    

#Read the contents of the chosen file
print "Opening " + sys.argv[1]
with open(sys.argv[1]) as csv:
    for line in csv:
        pointList.append(line)

#Initialize dimension variables  
dimensionLine = pointList.pop(0)
print dimensionLine
width, height = dimensionLine.split(',')
width = float(width)
height = float(height)

#Print the OK message
print ser.readline()

#Query the user for important information
printWidth = float(raw_input("What is the length of the print? "))
write(raw_input("What is the length of the string on the left? "))
print ser.readline()
write(raw_input("And the right? "))
print ser.readline()
time.sleep(1)

#Draw a few boxes around the perimeter
#of the image to ensure good quality
for i in range(1):
    pointList.insert(0,"0,{0}".format(height))
    pointList.insert(0,"{0},{1}".format(width,height))
    pointList.insert(0,"{0},0".format(width))
    pointList.insert(0,"0,0")


#Start printing!!  Yay!
for line in pointList:
    x, y = line.split(',')
    x = float(x)
    y = float(y)
    newLine = '@{0},{1}'.format(x/width*printWidth,y/height*(printWidth*height/width))
    print newLine
    write(newLine)
    while not ser.readline().startswith('g'):
        write(newLine)
        print 'I said ' + newLine

#Done printing
print 'Done!'
