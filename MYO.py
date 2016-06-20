import viz
import vizact
import oculus
import math
import linecache
import time
import os
import random
import sys
import viztask
import vizinfo
import os, sys, viz, vizact
sys.path.append(os.path.join('C:\Users\Bryton\Downloads\myo-python-master'))
sys.path.append(os.path.join('C:\Users\Bryton\Downloads\myo-sdk-win-0.8.1'))
import myo
from myo.lowlevel import pose_t, stream_emg
import math
from myo.six import print_
import random
import vizcam
SHOW_OUTPUT_CHANCE = .1
import oculus

viz.setMultiSample(4)
viz.go()
viz.phys.enable()
viz.phys.setGravity(0,0,0)
dojo = viz.add('ground_grass.osgb')
#dojo.setScale([20,0,20])
#frame = viz.add("frame.dae")
sky = viz.add('sky_day.osgb')


#-----------------
#-Main-View-Setup-
#-----------------

testsCompleted = 0 # amount of rounds completed, condition changes if 15 are completed
view = viz.MainView
view.collisionBuffer(1.8)
dinput = viz.add('DirectInput.dle')
joystick = dinput.addJoystick()
hmd = oculus.Rift()
ori = hmd.getSensor()

#def shoot():
#	pressed = joystick.getButtonState()
#	if pressed:
#		ball = viz.add("ball.wrl")
#		ball.color(viz.RED)
#		ball.ambient(6,1,6)
#		ball.setPosition([view.getPosition()[0], 1, view.getPosition()[2]])
#		ball.setEuler(ori.getEuler())
#		moveForward = vizact.move(0,0,50,100)
#		ball.add(moveForward)

def updateEuler():
	view.setEuler(ori.getEuler())
	
'''def updateJoy():
	elapsed = viz.elapsed()
	x,y,z = joystick.getPosition()
	move_amount = 5 * elapsed
	view.move([x*move_amount, 0, y*move_amount])
	view.setPosition([view.getPosition()[0], 1.8, view.getPosition()[2]])
'''	
#----------------------------
#-Gather Input before render-
#----------------------------

test = False
validID = False
subjectID = 1
while not (validID):
	try:
		#Prompt the user for an ID number
		subjectID = int(viz.input('Input Subject ID Number'))
		RESULTS_DIRECTORY = 'C:\Users\Bryton\Downloads\MyoResults2015'##CHANGE THIS
		#Validate the subject ID number
		outFilePath = '%s\Subject_%s.txt' %(RESULTS_DIRECTORY, str(subjectID))
		if os.path.exists(outFilePath) or subjectID is '':
			yes = viz.ask('The Subject ID Number ' + str(subjectID) + ' already exists. Pick a new one?')
			if not yes:
				raise 'Exiting...'
		else:
			validID = True
	except ValueError:
		print('Subject ID number must be an integer')
if test:
	subjectInitial = 't'
else:
	subjectInitial = (viz.input('Input subject inital'))
#Determine whether or not trial recording is enabled 
recordingEnabled = True
#print recordingEnabled
if recordingEnabled:
	dirPath = '.\Results\Subject_%s' % (str(subjectID))
	if(not os.path.exists(dirPath)):
		os.makedirs(dirPath)
	recordFile = open('Results\\Subject_%s\\bigHills_%s.txt' % (str(subjectID), subjectInitial), 'w')

#~~~~~
#~PHI~
#~~~~~

def phi(e):
	#print "ob:", e
	gaze_euler = viz.MainView.getEuler()
	gaze_euler = [math.radians(gaze_euler[0]),math.radians(gaze_euler[1]),math.radians(gaze_euler[2])]
	gaze_vector = [math.cos(gaze_euler[0])*math.cos(gaze_euler[1]),math.sin(gaze_euler[1]),math.sin(gaze_euler[0])*math.cos(gaze_euler[1])]
	cos_gaze_phi = math.sqrt(gaze_vector[0]*gaze_vector[0]+gaze_vector[2]*gaze_vector[2])/math.sqrt(gaze_vector[0]*gaze_vector[0]+gaze_vector[1]*gaze_vector[1]+gaze_vector[2]*gaze_vector[2])
	gaze_phi = math.acos(cos_gaze_phi)
	gaze_position = viz.MainView.getPosition()
	object_vector = [0,0,0]
	object_vector[0] = e[0] - gaze_position[0]
	object_vector[1] = e[1] - gaze_position[1]
	object_vector[2] = e[2] - gaze_position[2]
	cos_object_phi = math.sqrt(object_vector[0]*object_vector[0]+object_vector[2]*object_vector[2])/math.sqrt(object_vector[0]*object_vector[0]+object_vector[1]*object_vector[1]+object_vector[2]*object_vector[2])
	object_phi = math.acos(cos_object_phi)

	phi = gaze_phi - object_phi
	phi = math.degrees(phi)
	return phi

#--------------
#-Object-Setup-
#--------------

#The object sets
addresses0 = ["THEREALDOG.WRL", "thechair.WRL", "THEBARREL.WRL", "thebirds.WRL", "plant.WRL", "shield.WRL"]
addresses1 = ["bookshelf.WRL", "HARP.WRL", "THECHALICE.WRL", "THECLOCK.WRL", "THEBOX.WRL", "THEPHONEBOOTH.WRL"]
addresses2 = ["THEPIGGYBANK.WRL", "THETREASURECHEST.WRL", "THEURN.WRL", "THEWASHINGMACHINE.WRL", "watch.WRL", "wheelbarrow.ive"]

objectAddresses = [addresses0, addresses1, addresses2] #array of object sets
objects = [] #will contain actual objects
objectFiles = [] #will contain filenames and viz.add(obj) items
set = 2 #object set

#~~~~~~~~~~~~~~~~~~~~~~~~
#~File~Reading~Functions~
#~~~~~~~~~~~~~~~~~~~~~~~~

fileStartIndex = 0 #where to pick up reading the file
#LocationOrder reads lines from files that are randomized based on subjectID
def LocationOrder(fileName, lines = 1):
	MODerator = subjectID % 12 * lines
	list = []
	index = 0
	MODerator +=1
	for number_index in range(MODerator, MODerator + lines):
		if lines != 1:
			list.append([])
		real_line = linecache.getline(fileName, number_index)
		if real_line == '\n':
			real_line = linecache.getline(fileName, number_index+1)
		for character in real_line:
			if(character == ' '):
				pass
			elif(character == '\n'):
				pass
			else:
				if lines != 1:
					list[index].append(int(character))
				else:
					list.append(int(character))
		index += 1
	return list

def FileReader():
	global targetOrder, locationOrder
	targetOrder = LocationOrder("indexOrder.txt")
	locationOrder = LocationOrder("random.txt")

#------------------------
#-Master Location Arrays-
#------------------------

scale_h = 0
obj_h = 2 #will be hard coded in at end
xdif = 0.5 #not sure what this is for
scale = 5
slope35 = 0.7718232131 #slopefromthreeto5, also not sure what this is for
#masterObjectLocations is the locations for the 6 objects in the active set
masterObjectLocations = [[ -1.04082/scale, (obj_h-0.9)* scale_h, 24/scale ], [ -8.44218/scale, (obj_h-1)*scale_h, 4.5714/scale ], [ -15.2653/scale, (obj_h-1.3)*scale_h , -9.90476/scale ], [ 1.04082/scale, (obj_h-0.6)*scale_h, -11.8095/scale ], [ 12.6054/scale, (obj_h-1)*scale_h , -21.7143/scale ], [ (15.6122 + xdif)/scale, (obj_h-1.15)*scale_h, (-9.71429 + xdif * slope35)/scale ]]

test_h = 1.8*scale_h #also will be hard coded in
#masterTargetLocations is the locations for cylinders, height will be hard coded in
masterTargetLocations = [[ -17/scale, test_h, 1.333333/scale ],[ -7.17007/scale, test_h, -11.2381/scale ],[ 1.04082/scale, test_h, -20.8095/scale ],[ -18/scale, test_h, 9/scale ],[ 6.82313/scale, test_h, -3.80952/scale ],[ 15.2653/scale, test_h, 7.47619/scale ]]
targetLocations = [] #will contain the randomized targets from FileReader

offset = 0.5 #not sure about the math on this one
slope4 = -0.7224 #fournegrecslope, also not sure where this comes from
arrow_h = 1.8*scale_h #may have to hard code for height but also could just have the arrows in midair at the same level for all
#masterArrowLocations is the locations for the arrows
masterArrowLocations = [[(masterTargetLocations[0][0])/scale, arrow_h, (masterTargetLocations[0][2]+offset)/scale],[(masterTargetLocations[1][0] + math.cos(math.pi/4.25) * offset)/scale, arrow_h, (masterTargetLocations[1][2] + math.sin(math.pi/4.25) * offset)/scale],[(masterTargetLocations[2][0] + offset)/scale, arrow_h, (masterTargetLocations[2][2])/scale],[(masterTargetLocations[3][0])/scale, arrow_h, (masterTargetLocations[3][2] - offset)/scale],[(masterTargetLocations[4][0] - offset)/scale, arrow_h, (masterTargetLocations[4][2] - slope4 * offset)/scale],[(masterTargetLocations[5][0] - offset)/scale, arrow_h, (masterTargetLocations[5][2])/scale]]

#---------
#-Targets-
#---------

targetRotations = [45,180,30,310,100,350] #targetRotations is an array for how much to rotate each target each rotation
#masterTargetObjects: each index is a testing location, and the objects are the targets for that location
masterTargetObjects = [[0,1,2],[0,2,3],[2,3,5],[3,4,5],[0,3,5],[0,4,5]]
targetPosition = [0,0,0]
targetLocations = []
targetOrder = [1,2,0, 2,0,1, 2,0,1, 1,2,0, 2,0,1, 2,0,1] #order in which !!!!NOTSURE WILL COME BACK!!! probs from filereader
locationOrder = [1,4,2,3,5,0] #will be a 1d array because of separate code for each condition. each item is the number of the target location to go to
#the locationOrder will be randomized
targetCounter = 0 #which index of targetObjects
locationCounter = 0 #which index of locationOrder
currentTarget = 0 #not sure

def getCurrentTestingLocationOrder():
	global targetLocations
	global arrowLocations
	global targetObjects
	global locationOrder
	
	targetLocations = []
	arrowLocations = []
	targetObjects = []
	
	for i in range(len(masterTargetObjects)):
		arrowLocations.append([])
		targetLocations.append([])
		targetObjects.append([])
		
		currentTargetObjectIndex = locationOrder[i]
		currentTargetObject = masterTargetObjects[currentTargetObjectIndex]
		for j in range(len(masterTargetObjects[i])):
			indexTargetOrder = currentTargetObjectIndex * len(currentTargetObject) + j
			nextObjectIndex = targetOrder[indexTargetOrder]
			targetLocations[i].append(masterTargetLocations[locationOrder[i]][j])
			arrowLocations[i].append(masterArrowLocations[locationOrder[i]][j])
			targetObjects[i].append(currentTargetObject[nextObjectIndex])

#~~~~~~~~~~~~~~~~~~
#~Object~Functions~
#~~~~~~~~~~~~~~~~~~

def initializeObjectFiles():
	global objectFiles
	commonAddress='C:\Users\Bryton\Desktop\Terrain Vizard\TerrainStuff\\'
	for i in range(len(objectAddresses)):
		objectFiles.append([])
		for j in range(len(objectAddresses[i])):
			objectFiles[i].append(viz.add(commonAddress + objectAddresses[i][j]))
			objectFiles[i][j].visible(viz.OFF)
			
def initializeLocations():
	global objects, set
	for x in range(len(masterObjectLocations)):
		objects.append(objectFiles[set][x])
		objects[x].setScale([0.5,0.5,0.5])
		objects[x].setPosition(masterObjectLocations[x])
		objects[x].alpha = 0.0
		objects[x].visible(viz.ON)

def changeObjects():
	global fileStartIndex, objects, objectFiles, set
	set = (set + 1) % len(objectFiles)
	for x in range(len(objects)):
		temp = objectFiles[objectSet][x]
		temp.setPosition(objects[x].getPosition())
		objects[x].visible(viz.OFF)
		temp.visible(viz.ON)
		objects[x] = temp

#----------
#-Rotation-
#----------

rotation = 0 #will come back after def rotation():
startAngle = 0 #starting angle
turnAngle = 0 #angle after turning
angleIndex = 0 #not sure yet

off = 11		#precise amount off
ERROR = (43- off) * -1	#correct AMOUNT OF DEGREES to correct movement
currentYaw = 3.3	#angle of hmd accounting for error

#rotates objects by given angle about the origin
def rotate(angle, positions):
	#find the rotation matrix for the given angle
	radians = math.radians(angle)
	rotation = [[math.cos(radians), -math.sin(radians)], [math.sin(radians), math.cos(radians)]]
	newLocation = []
	#multiply all the locations by the matrix
	for x in range(len(positions)):
		newX = positions[x][0] * rotation[0][0] + positions[x][2] * rotation[0][1]
		newY = positions[x][0] * rotation[1][0] + positions[x][2] * rotation[1][1]
		newLocation.append([newX, positions[x][1], newY])
	#print newLocation
	return newLocation

#--------
#-States-
#--------

sight = False #will the subject be able to see when turning to face target object
currentState = 0 # 0=Observe 1=Walk 2=Turn 3=Reorient
locationFinished = False #I think this is whether or not all 3 have been tested at current spot

def changeState(state):
	global objects, objectLocations, targetLocations, targetRotations, currentTarget, rotation, startPosition, set
	global cylinder, arrow, targetToFace, objectFiles, startFileIndex, targetObjects, targetPosition, startAngle
	global recordFile, angleIndex, sun, monument
	#--------------------------------------------------------------
	#A state of 0 corresponds to showing all of the objects and no target
	if(state == 0):
		showScenery()
		for x in range(len(objects)):
				objects[x].visible(viz.ON)
		hideArrowCylinder()
	
	#--------------------------------------------------------------
	#A state of 1 corresponds to showing the target and waiting for the participant to
	#walk toward the target and face the right direction
	elif(state == 1):
		targetPosition = rotate(rotation, targetLocations)[currentTarget]
		targetRotation = targetRotations[currentTarget] + rotation
		cylinder.setPosition(targetPosition)
		angleArray = [45,90,45]
		arrowPosition = rotate(rotation, arrowLocations)[currentTarget]
		arrow.setPosition(arrowPosition)
		cylinder.setEuler(targetRotation)
		
		#show all of the objects and the cylinder and the arrow
		
		for x in range(len(objects)):
				objects[x].visible(viz.ON)
		showArrowCylinder()
	#--------------------------------------------------------------
	#A state of 2 corresponds to hiding the scene and waiting for the
	#participant to finish turning
	elif(state == 2):
		global startTime
		if not sight:
			hideScenery()
			for x in range(len(objects)):
				objects[x].visible(viz.OFF)
		hideArrowCylinder()
		startPosition = view.getPosition()
		viz.MainView.velocity(0,0,0)
		startAngle = view.getEuler()[0]#ERROR
		startTime = time.clock()
		viztask.schedule(ShowMessage('Please turn to face %s' % objectAddresses[set][(fileStartIndex + targetObjects[currentTarget][targetToFace]) % len(objectFiles[set])]))
		
	#--------------------------------------------------------------
	#A state of 3 corresponds to showing only the cylinder and arrow
	#so that the participant can be reoriented to the starting position
	elif(state == 3):
		if not sight:
			hideScenery()
			for x in range(len(objects)):
				objects[x].visible(viz.OFF)
		showArrowCylinder()

def statusUpdate():
	global  currentState, targetToFace, targetObjects, turnAngle, locationFinished, testsCompleted
	global currentTarget, set
	#Show the next target to walk toward
	#print "currentState:",currentState
	if(currentState == 0):
		currentState = 1
		if(recordingEnabled):
			recordFile.write('Target: %d\n' % currentTarget)
		changeState(currentState)
	#Hide the scene and let the participant turn
	elif(currentState == 1):
		targetToFace = -1
		currentState = 3
		#print 'Object Index: %d, Total Objects: %d' % (targetToFace, len(targetObjects[currentTarget]))
		changeState(currentState)
	#Show the arrow to reorient the participant
	elif(currentState == 2):
		global startTime
		timeDifference = time.clock() - startTime
		currentPosition = view.getPosition()
		movedTurned = False
		if startPosition != currentPosition:
			print "WARNING! STARTPOSITION IS NOT CURRENTPOSITION"
			movedTurned = True
		#calculate the angle turned and the angle desired
		objectPosition = rotate(rotation, masterObjectLocations)
		objectNumber = targetObjects[currentTarget][targetToFace]
		phi_stuff = masterObjectLocations[objectNumber]
		#print phi_stuff
		phi_error = phi(phi_stuff)
		print "phi_error:",phi_error
		destX = objectPosition[targetObjects[currentTarget][targetToFace]][0] - startPosition[0]
		destY = objectPosition[targetObjects[currentTarget][targetToFace]][2] - startPosition[2]
		mag = math.sqrt(destX*destX + destY*destY)
		normX = destX / mag
		normY = destY / mag
		startY = math.cos(math.radians(startAngle))
		startX = math.sin(math.radians(startAngle))
		endY = math.cos(math.radians(view.getEuler()[0]))#ERROR
		endX = math.sin(math.radians(view.getEuler()[0]))#ERROR
		dotNeeded = normX * startX + normY * startY
		dotTurned = startX * endX + startY * endY
		angleNeeded = math.degrees(math.acos(dotNeeded))
		angleTurned = math.degrees(math.acos(dotTurned))
		
		print 'Angle Needed: %f, Angle Turned: %f' % (angleNeeded, angleTurned)
		yaw_error = angleNeeded - angleTurned
		print "yaw_error:",yaw_error
		delim1 = '$'
		delim2 = '^'
		if(recordingEnabled):
			recordFile.write('%d,%s,%f,%f,%f,%f,%f,%f,%f, %f, %f, %s\n' % (objectNumber,
			objectAddresses[set][(fileStartIndex + targetObjects[currentTarget][targetToFace]) % len(objectFiles[set])],
			startPosition[0],startPosition[1],startPosition[2],startAngle,angleTurned,angleNeeded,timeDifference,yaw_error,phi_error,movedTurned))
		currentState = 3
		if(targetToFace + 1 >= len(targetObjects[currentTarget])):
			currentTarget = (currentTarget + 1) % len(targetObjects)
			locationFinished = True
		changeState(currentState)
		
	#Hide everything again and let the participant turn toward the new target
	elif(currentState == 3):
		if locationFinished:
			currentState = 0
			locationFinished = False
			changeState(currentState)
		targetToFace = targetToFace + 1
		testsCompleted += 1
		if(targetToFace < len(targetObjects[currentTarget])):
			currentState = 2
		#move on to next rotation
		else:
			currentState = 0
		changeState(currentState)

def redoTrial(trial):
	global currentState, currentTarget, targetToFace, locationFinished
	currentState = 0
	currentTarget = int(trial)
	locationFinished = False
	changeState(currentState)
	


#------
#-Time-
#------

startTime = time.clock() #initial time

#-----------------------------------
#-Cylinder-and-Arrow-Initialization-
#-----------------------------------

cylScale = (6,1.5,6)
cylinder = viz.add('cylinder.wrl')
cylinder.setPosition(masterTargetLocations[0]) #may have to modify this per environment
cylinder.setScale(cylScale)
cylinder.alpha(0.5) #dont know what alpha is
cylinder.visible(viz.OFF)
cylinder.disable(viz.INTERSECTION)
arrow = viz.add('arrow.wrl')
arrow.setScale(0.5,0.35,0.5)
arrow.setPosition(masterArrowLocations[0]) #why is this not masterArrowLocations[0]?
arrow.alpha(0.8)
arrow.visible(viz.OFF)
arrow.disable(viz.INTERSECTION)

def update():
	global currentState, arrow, cylinder, view, targetRotations, rotation, objects
	global targetObjects, currentTarget, targetToFace, targetPosition
	radius = 2
	if(currentState == 1 or currentState == 3):
		x = view.getPosition()[0] - targetPosition[0]
		y = view.getPosition()[2] - targetPosition[2]
		distSqrd = x*x + y*y
		if(distSqrd <= radius):
			cylinder.color(0,1,0)
			pointA = view.getPosition()[0],0,view.getPosition()[2] #+ math.sin(math.radians(currentYaw)) + math.cos(math.radians(currentYaw))   
			angle = get2Angle(view.getPosition(), pointA, arrow.getPosition())
			if(angle <= 15.0):
				arrow.color(0,1,0)
			else:
				arrow.color(1,0,0)
		else:
			cylinder.color(1,0,0)
			arrow.color(1,0,0)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~
#~Miscellaneous~Functions~
#~~~~~~~~~~~~~~~~~~~~~~~~~

def hideScenery():
	global dojo, sky
	dojo.visible(viz.OFF)
	sky.visible(viz.OFF)
	
def showScenery():
	global dojo, sky
	dojo.visible(viz.ON)
	sky.visible(viz.ON)
	
def hideArrowCylinder():
	global cylinder, arrow
	cylinder.visible(viz.OFF)
	arrow.visible(viz.OFF)
	
def showArrowCylinder():
	global cylinder, arrow
	cylinder.visible(viz.ON)
	arrow.visible(viz.ON)
	
def ShowMessage(mystring):
	info = vizinfo.add(mystring)
	yield viztask.waitTime(2)
	info.visible(0)
	
def printOrderObjects():
	for set in targetObjects:
		for obj in set:
			print objectAddresses[currentCondition][obj]
	
def objPos():
	global objects
	for x in range (len(objects)):
		print objects[x].getPosition()
		
def get2Angle(A, B, C):
	if (A == B and B == C and C == (0,0,0)):
		return 0
	vectorAB = B[0] - A[0], B[1] - A[1], B[2] - A[2]
	vectorAC = C[0] - A[0], C[1] - A[1], C[2] - A[2]
	
	dot = TwoDotProduct(vectorAB, vectorAC)
	magAB = TwoMagnitude(vectorAB)
	magAC = TwoMagnitude(vectorAC)
	try:
		theta = math.acos(dot / magAB / magAC)
	except ZeroDivisionError:
		return 0
	return math.degrees(theta)
	
def TwoDotProduct(vectA, vectB):
	xA = vectA[0]
	zA = vectA[2]
	
	xB = vectB[0]
	zB = vectB[2]
	
	return xA*xB + zA*zB
	
def TwoMagnitude(vect):
	x = vect[0]
	z = vect[2]
	return math.sqrt(x*x + z*z)



c = [0.0]
viz.go()
viz.collision(viz.ON)
hmd = oculus.Rift()
global navigationNode
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)
viewLink.preMultLinkable(hmd.getSensor())
if hmd.getSensor().getDisplayMode() == oculus.DISPLAY_DESKTOP:
	viz.window.setFullscreen(True)

'''def unitVector(x,y,z):
	vecMag = math.sqrt(x*x+y*y+z*z)
	return x/vecMag, y/vecMag, z/vecMag'''
	
def move(a,b,c):
	viz.move(a,b,c)


##viewLink.setEuler(viz.MainView.getEuler())
##viz.MainView.setEuler(0,0,0)
#Global variables
pi = 3.1452
gyro = [[0,0,0]]
gy = [0]
gy2 = [0]
gy3 = [0]
or1x = [0] #where you start
or1y = [0]
or1z = [0]
or1w = [0]
orx = [0]
ory = [0]
orz = [0]
orw = [0]
wingr = ""
wingrarm = ""
wingl = ""
winglarm = ""
hasfoundarm = [0,0]
center = [0,0,0]

pco = 0
prev = 0
# Setup Oculus Rift HMD
"""hmd = oculus.Rift()
if not hmd.getSensor():
	sys.exit('Oculus Rift not detected')"""
#Myo update function that updates every SHOW_OUTPUT_CHANCE seconds
def updateMyo(l):
	global prev
	global pco
	wingr = l[3]
	wingl = l[12]
	xvel = l[0][0] 
	yvel = l[1][0]
	zvel = l[2][0]
	oQuatl = [-l[7][0],-l[5][0],l[6][0],-l[4][0]]
	oQuatr = [-l[7][0],-l[5][0],-l[6][0],l[4][0]]
	offsetQuatl = [-l[11][0], -l[9][0], l[10][0], -l[8][0]]
	offsetQuatr = [-l[11][0], -l[9][0], -l[10][0], l[8][0]]
	wingl.setQuat(offsetQuatl)
	wingr.setQuat(offsetQuatr)
	wingl.setQuat(oQuatl)
	wingr.setQuat(oQuatr)
	winglQ = wingl.getQuat()
	wingrQ = wingr.getQuat()
	winglE = wingl.getEuler()
	wingrE = wingr.getEuler()
	if pco == 10:
		#print(winglE)
		#print(wingrE)
		pco = 0
	else:
		pco += 1
	
	#-----------------------------------------
	#This allows the movement, however it only goes forward on the x axis. It needs a bit tuning to go the direction the oculus is facing
	#-----------------------------------------
	joel = viz.MainView.getEuler()
	joel[0] += 180
	#navigationNode.runAction(update)
	viz.MainView.velocity(0,0,0)
	#if prev-winglE[1] > 0:
	c[0] = ((prev-winglE[1])/100)**2*100
	  
	navigationNode.setPosition(math.cos(hmd.getSensor().getEuler()[0]*pi/180-90)*c[0],0,-math.sin(hmd.getSensor().getEuler()[0]*pi/180-90)*c[0], viz.REL_PARENT)

	prev = winglE[1]
	wingl.setEuler(winglE[0]+230,-winglE[1],-winglE[2])
	wingr.setEuler(wingrE[0]+320,-wingrE[1],-wingrE[2])
	
	#Right now, point your arm away from the screen and press space to calibrate
	#The myo logo should be up with the wings pointing up your arm
	#by 'up' I mean it should point up and your palm should be dow
	
	
def matrixFromQuat(qx,qy,qz,qw):
	r = [[[1 - 2*qy**2 - 2*qz**2]	[2*qx*qy - 2*qz*qw]	    [2*qx*qz + 2*qy*qw]]
		[[2*qx*qy + 2*qz*qw]	    [1 - 2*qx**2 - 2*qz**2]	[2*qy*qz - 2*qx*qw]]
		[[2*qx*qz - 2*qy*qw]	    [2*qy*qz + 2*qx*qw]	    [1 - 2*qx**2 - 2*qy**2]]]
	return r
	
def multMatrices(X,Y):
	return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]
	
def addQuaternion(q,r):
	x = math.sin(math.asin(r[0])+math.asin(q[0]))
	y = math.sin(math.asin(r[1])+math.asin(q[1]))
	z = math.sin(math.asin(r[2])+math.asin(q[2]))
	w = math.sin(math.asin(r[3])+math.asin(q[3]))
	return [x,y,z,w] 
	
def multiplyQuaternion(q,r):
	x = r[0]*q[0] - r[1]*q[1] - r[2]*q[2] - r[3]*q[3]
	y = r[0]*q[1] + r[1]*q[0] - r[2]*q[3] + r[3]*q[2]
	z = r[0]*q[2] + r[1]*q[3] + r[2]*q[0] - r[3]*q[1]
	w = r[0]*q[3] - r[1]*q[2] + r[2]*q[1] + r[3]*q[0]
	return [x,y,z,w]
	
def quatToEuler(q): #doesn't work, setQuat and then getEuler on something instead ;)
	x = (math.atan2((q[0]*q[1]+q[2]*q[3]),1-2*(q[1]*q[1]+q[2]*q[2])) + pi)/(2*pi)*360
	y = (math.asin(2*(q[0]*q[2] - q[3]*q[1])) + pi)/(2*pi)*360
	z = (math.atan2(2*(q[0]*q[3] +q[1]*q[2]), 1-2*(q[2]*q[2]+q[3]*q[3])) + pi)/(2*pi)*360
	return [-x,y,-z]

def invertQuaternion(q):
	return [-q[0],-q[1],-q[2],q[3]]
r"""w
There can be a lot of output from certain da1a like acceleration and orientation.
This parameter controls the percent of times that data is shown.
"""
class Listener(myo.DeviceListener):
	# return False from any method to stop the Hub
	def on_connect(self, myo, timestamp):
		print_("Connected to Myo")
		myo.vibrate('short')
		myo.request_rssi()
		#print_(myo.mac_address())

	def on_rssi(self, myo, timestamp, rssi):
		print_("RSSI:", rssi)

	def on_event(self, event):
		r""" Called before any of the event callbacks. """

	def on_event_finished(self, event):
		r""" Called after the respective event callbacks have been
		invoked. This method is *always* triggered, even if one of
		the callbacks requested the stop of the Hub. """

	def on_pair(self, myo, timestamp):
		print_('Paired')
		print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")
		print_("Double tap enables EMG.")
		print_("Spreading fingers disables EMG.\n")

	def on_disconnect(self, myo, timestamp):
		print_('on_disconnect')

	def on_pose(self, myo, timestamp, pose):
		print_('on_pose', pose)
		if pose == pose_t.double_tap:
			print_("=" * 80)
			print_("Reset Orientation")
			or1x[0] = orx[0]
			or1y[0] = ory[0]
			or1z[0] = orz[0]
			or1w[0] = orw[0]
			#myo.set_stream_emg(stream_emg.enabled)
		elif pose == pose_t.fingers_spread:
			egg = 0
			#print_("=" * 80)
			#myo.set_stream_emg(stream_emg.disabled)

	def on_orientation_data(self, myo, timestamp, orientation):
		#show_output('orientation', orientation)
		#print_(orientation) #- The actual orientation quaternion that seems to be from -1 to 1
		#print_(orientation[0])
		orx[0] = orientation[0]
		ory[0] = orientation[1]
		orz[0] = orientation[2]
		orw[0] = orientation[3]
		if (or1x[0] == [0] and or1y[0] == [0] and or1z[0] == 0 and or1w[0] == [0]):
			or1x[0] = orientation[0]
			or1y[0] = orientation[1]
			or1z[0] = orientation[2]
			or1w[0] = orientation[3]

	def on_accelerometor_data(self, myo, timestamp, acceleration):
		show_output('acceleration', acceleration)

	def on_gyroscope_data(self, myo, timestamp, gyroscope):
		#show_output('gyroscope', gyroscope)
		gy[0] = gyroscope[0]
		gy2[0] = gyroscope[1]
		gy3[0] = gyroscope[2]
			

	def on_unlock(self, myo, timestamp):
		print_('unlocked')

	def on_lock(self, myo, timestamp):
		print_('locked')

	def on_sync(self, myo, timestamp, arm, x_direction):
		print_('synced', arm, x_direction)
		

	def on_unsync(self, myo, timestamp):
		print_('unsynced')
		
	def on_emg(self, myo, timestamp, emg):
		show_output('emg', emg)
		
def show_output(message, data):
	if random.random() < SHOW_OUTPUT_CHANCE: 
		return
		
def main():
	
	global wingl
	global wingr
	viz.cam.setHandler(vizcam.KeyboardCamera())
	myo.init()
	gyrolist = [[0,0,0]]

	viz.fov(150)
	#wingl.setScale([10,0.3,1])
	#wingl.setCenter([100,100,100])
	wingl.setEuler([0,90,0])
	wingl.collideSphere(0.5)
	lStartPOS = [ 0, 2.5, 2 ]
	wingl.setPosition( lStartPOS )
	#wingr.setScale([10,0.3,1])
	#wingr.setCenter([100,100,100])
	wingr.setEuler([0,90,0])
	wingr.collideSphere(0.5)
	rStartPOS = [ 0, 2.5, 2 ]
	wingr.setPosition( rStartPOS )


	hub = myo.Hub()
	hub.set_locking_policy(myo.locking_policy.none)
	hub.run(1000, Listener())
	vizact.ontimer(0.01 ,updateMyo, [gy, gy2, gy3, wingl, orx, ory, orz, orw, or1x, or1y, or1z, or1w, wingr])

	vizact.ontimer(0, updateEuler)

	FileReader()
	initializeObjectFiles()
	initializeLocations()
	getCurrentTestingLocationOrder()
	vizact.ontimer(0.1, update)

	
main()
