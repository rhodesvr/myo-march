# 7/22/14
# Issues: some unintentional movement still occurs, and changes in velocity should be more consistent
# Especially need to enable small steps and "fast" stepping in place of "big" stepping
# Movements close to the feet are causing fast movements - figure this out

# PROBLEM with figuring out which foot is "lame" is that the Kinect can't discern from the side which is the left and right foot.
# In order to simulate movement, 
# GOOD THING WE ARE MOVING TO GIT

import viz
import viztask
import vizjoy
import vizinfo
import vizshape
import vizact
import os
import math
import random
import datetime
import time 
import linecache
import oculus

#EXPERIMENT
#viz.go()
viz.go(viz.PROMPT)
# Get and validate a subject ID

test = True  # whether this is a test run or not
sight = test    # whether the display goes dark or not

validID = False
while not (validID):
	try:
		#Prompt the user for an ID number
		subjectID = int(viz.input('Input Subject ID Number'))
		RESULTS_DIRECTORY = 'C:\Users\Administrator\Downloads'
		#Validate the subject ID number
		outFilePath = '%s\Subject_%s.txt' %(RESULTS_DIRECTORY, str(subjectID))
		if os.path.exists(outFilePath) or subjectID is '':
			yes = viz.ask('The Subject ID Number ' + str(subjectID) + ' already exists. Pick a new one?')
			if not yes:
				raise 'Exiting...'
		else:
			validID = True
			print "we have a valid ide!"
	except ValueError:
		print('Subject ID number must be an integer')
if test:
	subjectInitial = 't'
else:
	subjectInitial = (viz.input('Input subject inital'))
#Determine whether or not trial recording is enabled 
recordingEnabled = viz.get(viz.OPTION2)
#print recordingEnabled
if recordingEnabled:
	print "we are recorders!"
	dirPath = './Results/Subject_%s' % (str(subjectID))
	if(not os.path.exists(dirPath)):
		print "making directory!"
		os.makedirs(dirPath)
	recordFile = open('Results\Subject_%s\Research2013_%s.txt ' % (str(subjectID), subjectInitial), 'w')
	

##################Get height###############################
if test:
	PART_HEIGHT = 2
else:
	PART_HEIGHT=viz.input("Enter Subject Height in Meters:")
	recordFile.write('Height:'+ str(PART_HEIGHT) + '\n')
	recordFile.write('Object,Object Name,StartX,StartY,StartZ,Start Angle,Angle Turned,Angle Needed,Time,turningerror,movedwhileTurning\n')
HEIGHT_TO_STRIDE = .414
strideLength = 1
print "strideLength = %f" %strideLength
#add the tracker on the hmd
#NAVIGATION METHOD
tracker = oculus.Rift()#CHANGE *******************???
''' *************************** KINECT CODE ***************************** '''
#myHead = vrpn.addTracker( 'Tracker0@localhost', HEAD)
HEAD = 0
NECK = 1
TORSO = 2
WAIST = 3
LEFTCOLLAR = 4
LEFTSHOULDER = 5
LEFTELBOW = 6
LEFTWRIST = 7
LEFTHAND = 8
LEFTFINGERTIP = 9
RIGHTCOLLAR = 10 
RIGHTSHOULDER = 11
RIGHTELBOW = 12
RIGHTWRIST = 13
RIGHTHAND = 14
RIGHTFINGERTIP = 15
LEFTHIP = 16
LEFTKNEE = 17
LEFTANKLE = 18
LEFTFOOT = 19
RIGHTHIP = 20
RIGHTKNEE = 21
RIGHTANKLE = 22
RIGHTFOOT = 23

# Store trackers, links, and vizshape objects
trackers = []
trackersB = []
# stores the trackers of whichever kinect we are using
trueTrackers = []

# Start vrpn
vrpn = viz.addExtension('vrpn7.dle') # CHANGE?
#desktop ip address
trackerLocationA = 'Tracker0@10.20.51.65'
#laptop ip address
trackerLocationB = 'Tracker0@10.20.32.135' 
# Trackers for specified bodyparts
HED = vrpn.addTracker(trackerLocationA, HEAD)
HEDB = vrpn.addTracker(trackerLocationB, HEAD)
RF = vrpn.addTracker(trackerLocationA, RIGHTFOOT)
LF = vrpn.addTracker(trackerLocationA, LEFTFOOT)
RK = vrpn.addTracker(trackerLocationA, RIGHTKNEE)
LK = vrpn.addTracker(trackerLocationA, LEFTKNEE)
RH = vrpn.addTracker(trackerLocationA, RIGHTHIP)
LH = vrpn.addTracker(trackerLocationA, LEFTHIP)
RS = vrpn.addTracker(trackerLocationA, RIGHTSHOULDER)
LS = vrpn.addTracker(trackerLocationA, LEFTSHOULDER)
Torso = vrpn.addTracker(trackerLocationA, TORSO)
TorsoB = vrpn.addTracker(trackerLocationB, TORSO)
RFb = vrpn.addTracker(trackerLocationB, RIGHTFOOT)
LFb = vrpn.addTracker(trackerLocationB, LEFTFOOT)
RKb = vrpn.addTracker(trackerLocationB, RIGHTKNEE)
LKb = vrpn.addTracker(trackerLocationB, LEFTKNEE)
RHb = vrpn.addTracker(trackerLocationB, RIGHTHIP)
LHb = vrpn.addTracker(trackerLocationB, LEFTHIP)
RSb = vrpn.addTracker(trackerLocationB, RIGHTSHOULDER)
LSb = vrpn.addTracker(trackerLocationB, LEFTSHOULDER)

#why do we need both above and below trackers?
for i in range (24):
	trackers.append(vrpn.addTracker(trackerLocationA,i))
	trackersB.append(vrpn.addTracker(trackerLocationB,i))
trueTrackers = trackers
falseTrackers = trackersB
#######################view stuff######################
#a bunch of redundency in this block
#ENVIRONMENT
view = viz.MainView
view.setPosition(0,1.8, 0)
view.collision(viz.OFF)
viz.eyeheight(PART_HEIGHT)
viz.MainView.setPosition(0,PART_HEIGHT,0)
#makes view follow movement of tracker

######################### step stuff ########################
#NAVIGATION METHOD
aIsTrue = False		#whether we are using trackerA or not

######################### Check Step stuff ####################
#EXPERIMENT, or maybe remove
toMove = 0
leftSteps = 0
rightSteps = 0
angleToMoveBy = 0.0
prevLeftAngle = -10.0
prevRightAngle = -10.0
thisLeftAngle = 0.0
thisRightAngle = 0.0
moveVelocity = 0.0
newVelocity = 0.0
velocities = []
VELOCITY_SIZE = 10
for x in range(VELOCITY_SIZE):
	velocities.append(0.0)
######################### angle stuff #######################
#a lot of these variables are not used, like yaws and aveYaw and flag_out
# will be moved between environment and navigation
finalYaw = 0
previousYaw = 0
turning = 0
stepCount = 0
rightAngleChangePerSecond = 0
leftAngleChangePerSecond = 0
rightRecordedACPS = rightAngleChangePerSecond
leftRecordedACPS = 1
rightAngleChangePerHalfSecond = 0
leftAngleChangePerHalfSecond = 0
leftRecordedACPHS = 0
rightRecordedACPHS = 0
######################## file stuff ###########################
#################### different file stuff #####################
#CHANGE****************************************************************************************************************************************************
#EXPERIMENT
comp = 2
if comp == 1:		#flower background    ? may need to switich comp1 and comp2 ?
	commonAddress = 'C:\\Users\\PC-Sanders1\\Desktop\\REALvsVIRTUAL\\Objects\\'#**
elif comp == 2:		#Gloomy
	commonAddress = 'C:\\Users\\Lenovo-PC\\Desktop\\REALvsVIRTUAL\\Objects\\'
else:
	commonAddress = 'C:\\Users\\Administrator\\Desktop\\REALvsVIRTUAL\\Objects\\'
	

"""****************** Addresses ******************"""
#could use a for loop, have an array for the specific filles and a
#string for the ending. then we could just display the name of the target

#address 0
#ENVIRONMENT
ojbectEnding = '.WRL'
dogAddress =  'THEREALDOG'
chairAddress =  'thechair'
barrelAddress =  'THEBARREL'
birdAddress =  'thebirds'
plantAddress =  'plant'
shieldAddress =  'shield'

#address 1
bookshelfAddress =  'bookshelf'
harpAddress =  'HARP'
chaliceAddress =  'THECHALICE'
clockAddress =  'THECLOCK'
crateAddress =  'THEBOX'
phoneboothAddress =  'THEPHONEBOOTH'

#address 2
piggybankAddress =  'THEPIGGYBANK'
treasurechestAddress =  'THETREASURECHEST'
urnAddress =  'THEURN'
washingmachineAddress =  'THEWASHINGMACHINE'
watchAddress =  'watch'
wheelbarrowAddress =  'wheelbarrow'

"""*****************************************************"""
#contains the objects pointed to in addresses
#ENVIRONMENT
addresses0 = [dogAddress, chairAddress, barrelAddress, birdAddress, plantAddress, shieldAddress]
addresses1 = [bookshelfAddress, harpAddress, chaliceAddress,clockAddress, crateAddress,phoneboothAddress]
addresses2 = [piggybankAddress, treasurechestAddress,urnAddress,washingmachineAddress,watchAddress, wheelbarrowAddress]


slopefromthreeto5 = .7718232131
#ENVIRONMENT
xdif = .5
objects = []
objectAddresses = [addresses0,addresses1, addresses2]
objectFiles = []

#ENVIRONMENT
objectHeight = 0
#Create locations for all of the objects in the envirnoment
masterObjectLocations = [[-1.04082, objectHeight, 24],
	[-8.44218,objectHeight, 4.5714],
	[-15.2653,objectHeight, -9.90476],
	[1.04082,objectHeight, -11.8095],
	[12.6054,objectHeight, -21.7143],
	[15.6122 + xdif,objectHeight, -9.71429 + xdif * slopefromthreeto5]]

#ENVIRONMENT
dojo = viz.addChild("ground_grass.osgb")
dojo.setScale(1.5,1.5,1.5)
sky = viz.addChild("sky_day.osgb")

#Add a joystick
#joystick = vizjoy.add()

objectSet = 0

#ENVIRONMENT
testingHeight = 0
#positions of cylinders for people to walk to and use to orient selves
masterTargetLocations = [[-17, testingHeight, 1.3333],
	[-7.17007, testingHeight, -11.2381],
	[1.04082, testingHeight, -23.8095],
	[8.21088, testingHeight, -15.619],
	[6.82313, testingHeight, -3.80952],
	[15.2653, testingHeight, 2.47619]]
targetLocations = []

#ENVIRONMENT
offset = 2
fournegrecslope = -.7224
arrowHeight = 1.5
#positions of arrows for people to face towards
masterArrowLocations = [[masterTargetLocations[0][0], arrowHeight, masterTargetLocations[0][2] + offset],
	[masterTargetLocations[1][0] + math.cos(math.pi / 4.25) * offset, arrowHeight, masterTargetLocations[1][2] + math.sin(math.pi / 4.25) * offset],
	[masterTargetLocations[2][0] + offset, arrowHeight, masterTargetLocations[2][2]],
	[masterTargetLocations[3][0], arrowHeight, masterTargetLocations[3][2] - offset],
	[masterTargetLocations[4][0] - offset, arrowHeight, masterTargetLocations[4][2] - fournegrecslope * offset],
	[masterTargetLocations[5][0] - offset, arrowHeight, masterTargetLocations[5][2]]]


#how much to rotate each target: target0 is rotated 45 degrees with each rotation, but this is wrong and isn't used
#ENVIRONMENT
targetRotations = [45, 180, 30, 310, 100, 350]
angleIndex = 0

#ENVIRONMENT
#from each spot corresponding to index in list, turn to these targets
#note that these are not randomized yet
masterTargetObjects = [[0,1,2],
	[0,2,3],
	[2,3,5],
	[3,4,5],
	[0,3,5],
	[0,4,5]]
targetObjects = []
targetPosition = [0,0,0]
#order in which to call the objects at the testing locations
#make sure that len(targetObjectsOrder) % len(targetObjects) == 0
#	and len(targetObjectsOrder) % len(targetObjects[0]) == 0
#NOTE: this is the order for the corresponding set for masterTargetObjects
#	ie, if the sixth set is first, the sixth set of the current targetOrder
#	would be used, not the first set
#The order for the trial is set in LocationOrder, FileReader, things like that
#ENVIRONMENT
targetOrder = [[1,2,0, 2,0,1, 2,0,1, 1,2,0, 2,0,1, 2,0,1],
	[2,1,0, 2,1,0, 0,2,1, 0,2,1, 0,1,2, 0,2,1],
	[0,1,2, 0,1,2, 0,1,2, 0,1,2, 0,1,2, 0,1,2]]

#order in which to go to testing locations
#	where locationCounter is incremented each time a location is finished (all 3 objects are called)
#	and targetCounter incrementes after each target
#ENVIRONMENT
locationOrder = [[1,4,2,3,5,0],
	[5,4,3,0,2,1],
	[0,1,2,3,4,5]]

#reset targetCounter and locationCounter after a condition is finished

# SPLIT BETWEEN ENVIRONMENT AND EXPERIMENT, MOSTLY EXPERIMENT AS NEEDS KNOWLEDGE OF NAVIGATION
condition = [0,1,2]		#order in which to do conditions: 0-joystick, 1-wip, 2-wipscaled
currentCondition = 0	#keeps track of current condition; also used in locationOrder[conditionCounter][locationCounter]

#to call something in targetObjects:
#targetObjects[locationOrder[conditionCounter][locationCounter]][targerOrder[conditionCounter][targetCounter]]

#ENVIRONMENT
currentTarget = 0
rotation = 0

#angle target starts out facing and angle target turns to
# ENVIRONMENT? OR NAV?
startAngle = 0

startTime = time.clock()

#ENVIRONMENT
#0-observe,1-walk,2-turn,3-reorient
currentState = 0
locationFinished = False

#ENVIRONMENT
#could make a scale variable to pass into setScale, see HopeLean.py
cylinder = viz.add('cylinder.wrl')
cylinder.setPosition(masterTargetLocations[0])
cylinder.setScale(4,3,4)
cylinder.alpha(0.5)
cylinder.visible(viz.OFF)
arrow = viz.add('arrow.wrl')
#arrow.setScale(0.05, 0.3, 0.05)
arrow.setPosition(0,0.7,0.25)
arrow.alpha(0.8)
arrow.visible(viz.OFF)

############################# File Functions ###############
#reads the file locationOrder. it returns a big array that has 3 smaller arrays of 5 numbers
#should be used for all methods reading in file
#might be read by experiment and passed to env? or just env?
def LocationOrder(fileName, lines = 1):
	MODerator = subjectID % 12 * lines
	list = []
	index = 0
	
	debug = False
	if debug:
		print MODerator
		print MODerator + lines
	
	MODerator +=1		#since line number starts with 1 instead of 0
	
	for number_index in range(MODerator, MODerator + lines):
		#print "inside for loop"
		if lines != 1:
			list.append([])
		
		real_line = linecache.getline(fileName, number_index)
		
		if real_line == '\n':
			real_line = linecache.getline(fileName, number_index+1)

		for character in real_line:
			#print "inside the other loop"
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
	
#assigns variables read from LocationOrderReader, 
#ConditionOrderReader, and TargetOrderReader
# AGAIN, MIGHT BE ENV OR MIGHT BE EXP
def FileReader():
	global condition, targetOrder, locationOrder
	condition = LocationOrder("conditions.txt")
	targetOrder = LocationOrder("indexOrder.txt",3)
	locationOrder = LocationOrder("random.txt",3)
	
	debug = False
	if debug:
		print "results of Location Order"
		print condition
		print targetOrder
		print locationOrder
##################################################################

# A BUNCH OF MATH, CAN PROBABLY BE MOVED TO ITS OWN FILE
#*****************************Angle Functions**********************
def unitVector(x,y,z):
	vecMag = math.sqrt(x*x+y*y+z*z)
	return x/vecMag, y/vecMag, z/vecMag

# function that takes three positions and returns angle between AB and AC
def getAngle(A, B, C):
	if (A == B and B == C and C == (0,0,0)):
		return 0
	vectorAB = B[0] - A[0], B[1] - A[1], B[2] - A[2]
	vectorAC = C[0] - A[0], C[1] - A[1], C[2] - A[2]
	
	dot = dotProduct(vectorAB, vectorAC)
	magAB = magnitude(vectorAB)
	magAC = magnitude(vectorAC)
	try:
		theta = math.acos(dot / magAB / magAC)
	except ZeroDivisionError:
		return 0
	return math.degrees(theta)
	
#function that takes in three positions and calculates the angle between AB and AC disregarding y-coord
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
	
#gets angle between two vectors
# CURRENTLY NOT USED
def getVAngle(vectA, vectB):
	if (vectA == vectB and vectB == (0,0,0)):
		return 0
	
	dot = dotProduct(vectA, vectB)
	magA = magnitude(vectA)
	magB = magnitude(vectB)
	
	try:
		theta = math.acos(dot / magA / magB)
	except ZeroDivisionError:
		return 0
	return math.degrees(theta)
	
#returns dot product disregarding y.
def TwoDotProduct(vectA, vectB):
	xA = vectA[0]
	zA = vectA[2]
	
	xB = vectB[0]
	zB = vectB[2]
	
	return xA*xB + zA*zB
	
#returns magnitude disregarding y
def TwoMagnitude(vect):
	x = vect[0]
	z = vect[2]
	return math.sqrt(x*x + z*z)	
	
#takes in a vector, returns magnitude of that vector
def magnitude(vect):
	x = vect[0]
	y = vect[1]
	z = vect[2]
	return math.sqrt(x*x + y*y + z*z)
	
	
#takes in two vectors, returns dot product of vectors
def dotProduct(vectA, vectB):
	xA = vectA[0]
	yA = vectA[1]
	zA = vectA[2]
	
	xB = vectB[0]
	yB = vectB[1]
	zB = vectB[2]
	
	return xA*xB + yA*yB + zA*zB

#takes in three points and returns normal vector, don't think this is used...
# CURRENTLY UNUSED
def crossProduct(pA, pB, pC):
	x1 = pB[0] - pA[0]
	y1 = pB[1] - pA[1]
	z1 = pB[2] - pA[2]
	
	x2 = pC[0] - pA[0]
	y2 = pC[1] - pA[1]
	z2 = pC[2] - pA[2]
	
	return y1 * z2 - z1 * y2, x1 * z2 - x2 * z1, x1 * y2 - x2 * y1

def rotateQuadrants(currX, currZ):
	#0.785 is 45 degrees in radians, which is needed to correct the HMD quadrants
	fortyfive = 0.785
	#print ("CurrX: " + str(currX) + " CurrZ: " + str(currZ))
	returnX = currX * math.cos(fortyfive) - currZ * math.sin(fortyfive)
	returnZ = currZ * math.cos(fortyfive) + currX * math.sin(fortyfive)
	return returnX, returnZ

#############################step detection and move functions###
#we are just using one kinect so that differences in coordinate systems do not
#create strange averages and impossible initialsteps. Though we could use rigid
#registration to correct the data, the result would be so similar to the first
#Kinect that we might as well use it. Also, rigid registration is used in check
#step, and the augmented data would correspond to the original initialstep

def distanceBetweenTwoPts(pointOne, pointTwo):
	dist = math.sqrt(((pointTwo[0]-pointOne[0])**2) + ((pointTwo[1]-pointOne[1])**2) + ((pointTwo[2]-pointOne[2])**2))
	return dist

curr = 40
oldDist = 0
headPosAll= falseTrackers[HEAD].getPosition()
headPosHold = headPosAll
#NAVIGATION
#whether to use trackerA or trackerB
def switchCam():
	global trueTrackers, aIsTrue
	oldTracker = aIsTrue	
	debug = False
	
	distA = abs(trackers[RIGHTHIP].getPosition()[0] - trackers[LEFTHIP].getPosition()[0])
	distB = abs(trackersB[RIGHTHIP].getPosition()[0] - trackersB[LEFTHIP].getPosition()[0])
	
	#if the distance between hips for trackerA < trackerB's distance, ie, side view
	if distA < distB:
		aIsTrue = True
		trueTrackers = trackers
		falseTrackers = trackersB
	else:
		aIsTrue = False
		trueTrackers = trackersB
		falseTrackers = trackers
	
	if debug and oldTracker is not aIsTrue:
		print "we are using tracker A: ", aIsTrue
		
wait = True
def checkTurning():
	global previousYaw, turning, wait
	
	angleThreshold = 3
	#if turning and wait then wait to update turning
	if turning and wait:
		wait = False
	#else either we are ready or we weren't turning
	else:
		#see HopeLean for a better method to check if two angles are within threshold
		turning = ((finalYaw < (previousYaw - angleThreshold)) or (finalYaw > (previousYaw + angleThreshold)))
		previousYaw = finalYaw
		wait = turning
	
off = 11		#precise amount off
ERROR = (43- off) * -1	#AMOUNT OF DEGREES to correct movement
def angleChangePerSecond():
	global rightAngleChangePerSecond, leftAngleChangePerSecond
	global leftRecordedACPS, rightRecordedACPS
	rightRecordedACPS = rightAngleChangePerSecond
	leftRecordedACPS = leftAngleChangePerSecond
	rightAngleChangePerSecond = 0
	leftAngleChangePerSecond = 0

def angleChangePerHalfSecond():
	global rightAngleChangePerHalfSecond, leftAngleChangePerHalfSecond
	global leftRecordedACPHS, rightRecordedACPHS
	rightRecordedACPHS = rightAngleChangePerHalfSecond
	leftRecordedACPHS = leftAngleChangePerHalfSecond
	rightAngleChangePerHalfSecond = 0
	leftAngleChangePerHalfSecond = 0

minimumAngleChange = 40
def anyAboveThreshold():
	if rightRecordedACPS > minimumAngleChange or leftRecordedACPS > minimumAngleChange:
		return True
	else:
		return False

maxLeftAngle = 0.0
maxRightAngle = 0.0
prevYaw = -10
rightMakeUp = False
leftMakeUp = False
lameFoot = False
minLeftAnkleHeight = 10.0
maxLeftAnkleHeight = 0.0
minRightAnkleHeight = 10.0
maxRightAnkleHeight = 0.0
inLeftStep = False
inRightStep = False
ifEverLameFoot = False
#keep in mind that "right" and "left" are not necessarily correct terms
#The side Kinect can often not distinguish between the two

#to do next: implement currentYaw - prevYaw > some threshold check
#NAVIGATION
def checkStep():
	global finalYaw, leftSteps, rightSteps
	global lameFoot, inLeftStep, inRightStep
	global prevYaw 
	global maxLeftAngle, maxRightAngle
	global prevLeftAngle, prevRightAngle
	global angleToMoveBy, moveVelocity, newVelocity
	global trueTrackers, rightMakeUp, leftMakeUp, ifEverLameFoot
	global toMove 
	global rightAngleChangePerSecond, leftAngleChangePerSecond, rightAngleChangePerHalfSecond, leftAngleChangePerHalfSecond
	global minLeftAnkleHeight, maxLeftAnkleHeight, minRightAnkleHeight, maxRightAnkleHeight
	
	finalYaw = tracker.getData()[3] + ERROR
	currentYaw = view.getPosition()[0] + math.sin(math.radians(view.getEuler()[0] + ERROR)),0,
	view.getPosition()[2] + math.cos(math.radians(view.getEuler()[0] + ERROR))
	if prevYaw == -10:
		prevYaw = currentYaw
	#currentYawChange = currentYaw - prevYaw
	# make sure we are using the right trackers
	switchCam()
	
	angleToMoveBy = view.getEuler()[0]

	
	angleInfo = True
	#check to make sure data is accurate
	leftFootHeight = trueTrackers[LEFTANKLE].getPosition()[1]
	leftKneeHeight = trueTrackers[LEFTKNEE].getPosition()[1]
	leftHipHeight = trueTrackers[LEFTHIP].getPosition()[1]
	rightFootHeight = trueTrackers[RIGHTANKLE].getPosition()[1]
	rightKneeHeight = trueTrackers[RIGHTKNEE].getPosition()[1]
	rightHipHeight = trueTrackers[RIGHTHIP].getPosition()[1]

	debugFoot = 1

	#check to make sure that nothing crazy is going on
	if(leftFootHeight > leftHipHeight or rightFootHeight > rightHipHeight or leftFootHeight > leftKneeHeight or rightFootHeight > rightKneeHeight):
		return
		
	#get angle of left and right legs
	sideAngleR = getAngle(trueTrackers[RIGHTHIP].getPosition(), trueTrackers[RIGHTKNEE].getPosition(), trueTrackers[RIGHTSHOULDER].getPosition())
	sideAngleL = getAngle(trueTrackers[LEFTHIP].getPosition(), trueTrackers[LEFTKNEE].getPosition(), trueTrackers[LEFTSHOULDER].getPosition())
	frontAngleR = getAngle(falseTrackers[RIGHTHIP].getPosition(), falseTrackers[RIGHTKNEE].getPosition(), falseTrackers[RIGHTSHOULDER].getPosition())
	frontAngleL = getAngle(falseTrackers[LEFTHIP].getPosition(), falseTrackers[LEFTKNEE].getPosition(), falseTrackers[LEFTSHOULDER].getPosition())
	if not lameFoot:
		useAngleR = sideAngleR
		useAngleL = sideAngleL
	else:
		useAngleR = frontAngleR
		useAngleL = frontAngleL

	#get the beginning of the step and then the max?
	#or more simple method: if one ankle is a bit higher than the other, enable double stepping?
	trueRightAnkle = falseTrackers[RIGHTANKLE].getPosition()[1]
	trueLeftAnkle = falseTrackers[LEFTANKLE].getPosition()[1]

	if prevLeftAngle < 0:
		prevLeftAngle = useAngleL
		thisLeftAngle = useAngleL
	else:
		thisLeftAngle = useAngleL
	if prevRightAngle < 0:
		prevRightAngle = useAngleR
		thisRightAngle = useAngleR
	else:
		thisRightAngle = useAngleR
	#Consider getting rid of "filter"
	divideParameter = 500
	debugMove = 1
	leftAngleChange = abs(thisLeftAngle - prevLeftAngle)
	rightAngleChange = abs(thisRightAngle - prevRightAngle)
	tooMuch = 20
	rightAngleChangePerSecond += rightAngleChange
	leftAngleChangePerSecond += leftAngleChange
	rightAngleChangePerHalfSecond += rightAngleChange
	leftAngleChangePerHalfSecond += leftAngleChange

	keepGoing = anyAboveThreshold()
	if leftAngleChange > tooMuch or rightAngleChange > tooMuch or not keepGoing \
		and not leftMakeUp and not rightMakeUp:
		maxLeftAngle = 0.0
		maxRightAngle = 0.0
		#reset prevLeft and prevRight here?
		toMove = 0.0
		prevLeftAngle = thisLeftAngle
		prevRightAngle = thisRightAngle
		maxRightAnkleHeight = 0.0
		minRightAnkleHeight = 10.0
		maxLeftAnkleHeight = 0.0
		minLeftAnkleHeight = 10.0
		return
	if thisLeftAngle > maxLeftAngle:
		maxLeftAngle = thisLeftAngle
	if thisRightAngle > maxRightAngle:
		maxRightAngle = thisRightAngle
	if trueRightAnkle > maxRightAnkleHeight:
		maxRightAnkleHeight = trueRightAnkle
	if trueRightAnkle < minRightAnkleHeight:
		minRightAnkleHeight = trueRightAnkle
	if trueLeftAnkle > maxLeftAnkleHeight:
		maxLeftAnkleHeight = trueLeftAnkle
	if trueLeftAnkle < minLeftAnkleHeight:
		minLeftAnkleHeight = trueLeftAnkle

	maxThreshold = 15
	maxDivide = 500
	if rightAngleChange >= leftAngleChange:
		# and rightAngleChange > 6:
		if debugMove:
			print "old right: ", prevRightAngle
			print "new right: ", thisRightAngle
			print "right Change: ", rightAngleChange
			print "max right: ", maxRightAngle
			#always prints zero
			#print "rightSteps: ", rightSteps
		#next: incorporate max into velocity equation
		if maxRightAngle - thisRightAngle < maxThreshold:
			divideParameter *= maxDivide
			inRightStep = False
		else:
			inRightStep = True
		newVelocity = rightAngleChange * (maxRightAngle - thisRightAngle) / divideParameter
	else:
		if debugMove:
			print "old left: ", prevLeftAngle
			print "new left: ", thisLeftAngle
			print "left Change: ", leftAngleChange
			print "max left: ", maxLeftAngle
		#next: incorporate max into velocity equation
		if maxLeftAngle - thisLeftAngle < maxThreshold:
			divideParameter *= maxDivide
			inLeftStep = False
		else:
			inLeftStep = True
		newVelocity = leftAngleChange * (maxLeftAngle - thisLeftAngle) / divideParameter

	if debugFoot:
		print "Right steps: ", rightSteps
		print "Left steps: ", leftSteps
		print "lameFoot: ", lameFoot

	prevLeftAngle = thisLeftAngle
	prevRightAngle = thisRightAngle
	for x in range(VELOCITY_SIZE - 1):
		velocities[x] = velocities[x+1]
		velocities[VELOCITY_SIZE - 1] = newVelocity
		total = 0.0
		for x in range(VELOCITY_SIZE - 1):
			total = total + velocities[x]
		total = total + newVelocity
		#set moveVelocity to the average of the velocities
		moveVelocity = total / (VELOCITY_SIZE + 1)
	if debugMove:
		print "Move by ", moveVelocity
	# Increment toMove only a little for the first couple of steps, and then increase it to enable fluid movement
	# (This helps enable more precise, localized movement and minimizes the amount moved on unintentional steps)
	if divideParameter > 500:
		toMove += 0.003
	else:
		toMove += 0.3

	if (abs(trueLeftAnkle - maxLeftAnkleHeight) < 0.5 and not (inRightStep or inLeftStep) and \
		abs(minLeftAnkleHeight - maxLeftAnkleHeight) > 0.01) or (abs(trueRightAnkle - maxRightAnkleHeight) < 0.5 \
		and not (inRightStep or inLeftStep) and abs(minRightAnkleHeight - maxRightAnkleHeight) > 0.01):
		lameFoot = True
		ifEverLameFoot = True
		if debugMove:
			print "@@@@@@@@@@@@@@@@LAME FOOT@@@@@@@@@@@@@@@@@@"
	else:
		lameFoot = False
		print "ifEverLameFoot is ", ifEverLameFoot
		print "abs(trueLeftAnkle - maxLeftAnkleHeight)", abs(trueLeftAnkle - maxLeftAnkleHeight)
		print "abs(minLeftAnkleHeight - maxLeftAnkleHeight)", abs(minLeftAnkleHeight - maxLeftAnkleHeight)
		print "abs(trueRightAnkle - maxRightAnkleHeight", abs(trueRightAnkle - maxRightAnkleHeight)
		print " abs(minRightAnkleHeight - maxRightAnkleHeight)",  abs(minRightAnkleHeight - maxRightAnkleHeight)
		print "inRightStep or inLeftStep", inRightStep or inLeftStep
		
newX = 0.0
newY = 0.0

# ENVIRONMENT
def moveNow():
	global toMove, turning, rightSteps, leftSteps
	if pause:
		return
	elif toMove > 0 and not turning and moveVelocity > 0:
		oldX = view.getPosition()[0]
		oldY = PART_HEIGHT
		oldZ = view.getPosition()[2]
		# "angle To Move By" restricts movement of the viewpoint to moving from the original point
		# at which the person started moving. This shouldn't cause too much of an issue, since
		# movement is stopped upon 3 degrees of turning per 1/5 of a second anyway.
		# But if it does, try to split the difference between the old and new yaw angles using gazeAngle things

		#could also get average velocity
		newX = oldX + moveVelocity * math.sin(math.radians(angleToMoveBy + ERROR))
		newZ = oldZ + moveVelocity * math.cos(math.radians(angleToMoveBy + ERROR))
		#subtract the amount just moved from the total amount needed to move
		# toMove -= 1.15 * math.sqrt((oldX - newX)**2 + (oldZ - newZ)**2)
		toMove -= math.sqrt((oldX - newX)**2 + (oldZ - newZ)**2)
		if toMove < 0:
			toMove = 0
		view.setPosition(newX, oldY, newZ)
	else:
		#can't reset anything here besides toMove -- it happens too often
		toMove = 0
		rightSteps = 0
		leftSteps = 0

pause = False
	
#--------------------------------------------------------------	
#this function rotates the position of the objects by the
#given amount around the origin
#--------------------------------------------------------------
# ENVIRONMENT
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
		
	return newLocation

	
#------------------------------------
#this function switches out the set of objects used
#-----------------------------------------------------
# ENVIRONMENT
def changeObjects():
	global objects, objectFiles, objectSet
	debug = False
	objectSet = (objectSet + 1) % len(objectFiles)
	if debug:
		print "here is len(objects): %d" %len(objects)
	for x in range(len(objects)):
		temp = objectFiles[objectSet][x]
		temp.setPosition(objects[x].getPosition())
		objects[x].visible(viz.OFF)
		temp.visible(viz.ON)
		objects[x] = temp
		
#sets order in which to go to testing locations and in which order to call objects for each
# testing location
# ENVIRONMENT
def getCurrentTestingLocationOrder():
	global targetLocations
	global arrowLocations
	global targetObjects
	
	debug = False
	info = True
	targetLocations = []
	arrowLocations = []
	targetObjects = []
	
	currentLocationOrder = locationOrder[currentCondition]
	if debug:
		print "currentLocationOrder",currentLocationOrder
	#for each condition
	for i in range(len(masterTargetObjects)):
		#make a new array
		arrowLocations.append([])
		targetLocations.append([])
		targetObjects.append([])
		
		currentTargetObjectIndex = currentLocationOrder[i]
		currentTargetObject = masterTargetObjects[currentTargetObjectIndex]
		if debug:
			print currentTargetObject
			print currentTargetObjectIndex
		#for each object in array
		for j in range(len(masterTargetObjects[i])):
			indexTargetOrder = currentTargetObjectIndex * len(currentTargetObject) + j
			nextObjectIndex = targetOrder[currentCondition][indexTargetOrder]
			if debug:
				print indexTargetOrder
				print nextObjectIndex
			#add objects
			targetLocations[i].append(masterTargetLocations[locationOrder[currentCondition][i]][j])
			arrowLocations[i].append(masterArrowLocations[locationOrder[currentCondition][i]][j])
			targetObjects[i].append(currentTargetObject[nextObjectIndex])
	if debug:
		print targetLocations
		print arrowLocations
		print targetObjects
		
	if info:
		print targetObjects
		print locationOrder[currentCondition]
		printOrderObjects()
		
#function to make changing conditions easier
# PROBABLY SPLIT BETWEEN EXPERIMENT AND ENVIRONMENT
def changeConditions():
	global currentState, targetToFace, currentTarget
	global view, currentCondition
	
	#hide objects
	keyEvent('h')
	#get new objects
	keyEvent('o')
	#can uncomment and 'rotate', but with grass environment it doesn't really make a difference
	#keyEvent('r')
	#do not uncomment this unless account for names not matching objects
	#keyEvent('m')
	
	currentTarget =  0
	currentState = targetToFace = 0
	#start at beginning of the new condition
	changeState(currentState)

	#reset the subject height
	view.setPosition(0,PART_HEIGHT,0)
	
	angleArray = [45,90,45]
	#currentviewYaw = view.getEuler()[0]
	hackoffset = 0
	if (angleIndex == 1):
		hackoffset = 45
	#turn the person around a little, meant to have them always face the front of the dojo, but
	# doesn't matter much in grass plain
	view.setEuler(angleArray[angleIndex] + hackoffset,0,0)
	
	currentCondition += 1
	if currentCondition > 2:
		print "finished with testing!"
		currentCondition %= 3
	getCurrentTestingLocationOrder()
		
#--------------------------------------------------------------
#this function updates the scene to correspond with the given
#state of the experiment
#--------------------------------------------------------------
# AGAIN, CLOSELY INTERTWINED BETWEEN EXPERIMENT AND ENVIRONMENT
def changeState(state):
	global targetLocations, targetRotations, currentTarget, rotation, startPosition, objectSet
	global cylinder, arrow, targetToFace, objectFiles, targetObjects, targetPosition, startAngle
	global recordFile
	#print 'Changing state to: %d' % state
	debug = False
	#--------------------------------------------------------------
	#A state of 0 corresponds to showing all of the objects and no target
	if(state == 0):
		if recordingEnabled:
			recordFile.write('currentCondition: %d\n' %condition[currentCondition])
		#see HopeLean for a better way to hide scenery and cylinder
		dojo.visible(viz.ON)
		sky.visible(viz.ON)
		keyEvent('s')
		cylinder.visible(viz.OFF)
		arrow.visible(viz.OFF)
	
	#--------------------------------------------------------------
	#A state of 1 corresponds to showing the target and waiting for the participant to
	#walk toward the target and face the right direction
	elif(state == 1):
		if debug:
			print 'Target Number: %d' % currentTarget
			#Calculate the position of the cylinder
			print targetLocations
		targetPosition = rotate(rotation, targetLocations)[currentTarget]
		targetRotation = targetRotations[currentTarget] + rotation
		cylinder.setPosition(targetPosition)
		
		angleArray = [45,90,45]
		#Calculate the position of the arrow
		arrowPosition = rotate(rotation, arrowLocations)[currentTarget]
		arrow.setPosition(arrowPosition)
		cylinder.setEuler(targetRotation)
		
		#show all of the objects and the cylinder and the arrow
		dojo.visible(viz.ON)
		sky.visible(viz.ON)
		keyEvent('s')
		cylinder.visible(viz.ON)
		arrow.visible(viz.ON)
		if debug:
			print "arrow should be on"
		
	#--------------------------------------------------------------
	#A state of 2 corresponds to hiding the scene and waiting for the
	#participant to finish turning
	elif(state == 2):
		global startTime
		if not sight:
			dojo.visible(viz.OFF)
			sky.visible(viz.OFF)
			keyEvent('h')
		cylinder.visible(viz.OFF)
		arrow.visible(viz.OFF)
		startPosition = view.getPosition()
		startAngle = view.getEuler()[0] + ERROR
		startTime = time.clock()
		
		if debug:
			#this is a very important print statement
			print 'StartIndex: %d, Index: %d' % (targetObjects[currentTarget][targetToFace]) % len(objectFiles[objectSet]))
		
		viztask.schedule(ShowMessage('Please turn to face %s' % objectAddresses[objectSet][(targetObjects[currentTarget][targetToFace]) % len(objectFiles[objectSet])]))
		
	#--------------------------------------------------------------
	#A state of 3 corresponds to showing only the cylinder and arrow
	#so that the participant can be reoriented to the starting position
	elif(state == 3):
		if not sight:
			dojo.visible(viz.OFF)
			sky.visible(viz.OFF)
			keyEvent('h')
		cylinder.visible(viz.ON)
		arrow.visible(viz.ON)
		if debug:
			print "arrow should be on"
		
#DO WE ACTUALLY USE THIS?
# AND I GUESS EXPERIMENT... OR ENVIRONMENT... BUT PROBABLY EXPERIMENT
def ShowMessage(mystring):
	info = vizinfo.add(mystring)
	#change param to translate to change where message is displayed
	info.translate(0.5,0.5)
	yield viztask.waitTime(2)
	info.visible(0)
	
# ENVIRONMENT
def printOrderObjects():
	for set in targetObjects:
		for obj in set:
			print objectAddresses[currentCondition][obj]
		
# currently not used
def objPos():
	global objects
	for x in range (len(objects)):
		print objects[x].getPosition()
	
#if something happens and you need to redo a trial, use this function (by pressing a number key
# also see HopeLean for a more human friendly way (inside of keyEvent)
# A TOUGH BALANCE BETWEEN ENVIRONMENT AND EXPERIMENT
def redoTrial(trial):
	global currentState, currentTarget, targetToFace, locationFinished
	
	#make arrows disappear and display objects
	currentState = 0
	
	#make arrow and cylinder position that of trial to redo
	currentTarget = trial
	
	#reset so that we start at the beginning again, it should be -1
	#no need to have it if set global currentState to 0
	#targetToFace = -1
	
	locationFinished = False
	
	changeState(currentState)

#--------------------------------------------------------------
#this function handles all of the keyboard input
#--------------------------------------------------------------

#EXPERIMENT
outFile = open('angleChanges.txt', 'w')
def keyEvent(key):
	global rotation, objects, cylinder, arrow, currentTarget, targetRotations, objectFiles, objectSet
	global startPosition, startAngle, targetPosition, recordingEnabled, recordFile
	global targetLocations, targetObjects
	global PART_HEIGHT
	global angleIndex
	global example, horse, exapmleCylinder
	global locationFinished
	

	#hide the objects
	if(key == 'h'):
		for x in range (len(objects)):
			objects[x].visible(viz.OFF)
			
	#show the objects
	elif(key == 's'):
		for x in range (len(objects)):
			objects[x].visible(viz.ON)
			
	#switch the set of objects
	elif(key == 'o'):
		print"inside of o"
		changeObjects()
	
	#when a condition is done, push the almighty button
	elif(key == 'a'):
		changeConditions()

	#update the state
	elif(key == ' '):
		global  currentState, targetToFace, targetObjects, turnAngle
		
		debug = False
		if debug:
			print "current view angle: ", view.getEuler()[0] + ERROR
			print currentState
		#Show the next target to walk toward
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
				print startPosition
				print view.getPosition()
			#calculate the angle turned and the angle desired
			objectPosition = rotate(rotation, masterObjectLocations)
			objectNumber = targetObjects[currentTarget][targetToFace]
			destX = objectPosition[targetObjects[currentTarget][targetToFace]][0] - startPosition[0]
			destY = objectPosition[targetObjects[currentTarget][targetToFace]][2] - startPosition[2]
			mag = math.sqrt(destX*destX + destY*destY)
			normX = destX / mag
			normY = destY / mag
			startY = math.cos(math.radians(startAngle))
			startX = math.sin(math.radians(startAngle))
			endY = math.cos(math.radians(view.getEuler()[0] + ERROR))
			endX = math.sin(math.radians(view.getEuler()[0] + ERROR))
			dotNeeded = normX * startX + normY * startY
			dotTurned = startX * endX + startY * endY
			angleNeeded = math.degrees(math.acos(dotNeeded))
			angleTurned = math.degrees(math.acos(dotTurned))
			
			#print 'StartX: %f, StartY: %f, DestX: %f, DestY: %f, EndX: %f, EndY: %f' % (startX, startY, destX, destY, endX, endY)
			print 'Angle Needed: %f, Angle Turned: %f' % (angleNeeded, angleTurned)
			
			delim1 = '$'
			delim2 = '^'
			
			if(recordingEnabled):
				recordFile.write('%d,%s,%f,%f,%f,%f,%f,%f,%s%f%s, %s%f%s, %s\n' % (objectNumber,
				objectAddresses[currentCondition][(targetObjects[currentTarget][targetToFace]) % len(objectFiles[objectSet])],
				startPosition[0],startPosition[1],startPosition[2],startAngle,angleTurned,angleNeeded,delim1,timeDifference,delim1,delim2,abs(angleNeeded - angleTurned),delim2,movedTurned))
			
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
			if debug:
				print "here is target to face: ",targetToFace

			if(targetToFace < len(targetObjects[currentTarget])):
				currentState = 2
				if debug:
					print 'Object Index: %d, Total Objects: %d' % (targetToFace, len(targetObjects[currentTarget]))
			#move on to next rotation
			else:
				print "move onto next location!"
				currentState = 0
				
			changeState(currentState)
			
	#prohibit movement
	elif key == 'p':
		global pause
		pause = not pause

	elif key == 'u':
		outFile.write("Unintentional: \n")
		outFile.write('leftRecordedACPHS: %d\n' %leftRecordedACPHS)
		outFile.write('leftRecordedACPS: %d\n' %leftRecordedACPS)
		outFile.write('rightRecordedACPHS: %d\n' %rightRecordedACPHS)
		outFile.write('rightRecordedACPS: %d\n' %rightRecordedACPS)
		outFile.write('\n')

	elif key == 'i':
		outFile.write("Intentional: \n")
		outFile.write('leftRecordedACPHS: %d\n' %leftRecordedACPHS)
		outFile.write('leftRecordedACPS: %d\n' %leftRecordedACPS)
		outFile.write('rightRecordedACPHS: %d\n' %rightRecordedACPHS)
		outFile.write('rightRecordedACPS: %d\n' %rightRecordedACPS)
		outFile.write('\n')
		
	elif key == 'd':
		pos = view.getPosition()
		update = vizact.goto([pos[0], pos[1] -1, pos[2]], 2, mode = viz.SPEED, ori_mask = viz.BODY_ORI)
		viz.MainView.runAction(update)
		
	#toggle on and off the example
	elif key == 'e':
		example = not example
		if example:
			keyEvent('h')
			horse = viz.add('horse.wrl')
			horse.setPosition(-2,0,2)
			horse.visible(viz.ON)
			exapmleCylinder = viz.add('cylinder.wrl')
			exapmleCylinder.alpha(0.5)
			exapmleCylinder.setScale(4,3,4)
			exapmleCylinder.color(1,0,0)
			exapmleCylinder.setPosition(3, 0, 3)
			exapmleCylinder.visible(viz.ON)
		else:
			keyEvent('s')
			horse.remove()
			exapmleCylinder.remove()
	#if trial was messed up, redo that trial afterwards by pressing the number corresponding to that trial
	elif key == '1' or key == '2' or key == '3' or key == '3' or key == '4' or key == '5' or key == '0':
		redoTrial(int(key))
		#from HopeLean,
		#redoTrial(int(key) - 1)
		#and replace '0' with '6'
	
	#if we push any other key, print out position of person
	else:
		print view.getPosition()
horse = 0
exapmleCylinder = 0
"""/////////////////////////////////////////////////////////////////////////////////////"""
#EXPERIMENT
def initializeLocations():
	global objects
	

	for x in range(len(masterObjectLocations)):
		objects.append(objectFiles[objectSet][x])
		
		objects[x].setPosition(masterObjectLocations[x])
		objects[x].alpha = 0.0
		objects[x].visible(viz.ON)

#initialize all of the objects, make them invisible too
#EXPERIMENT
def initializeObjectFiles():
	global objectFiles
	
	for i in range(len(objectAddresses)):
		objectFiles.append([])
		for j in range(len(objectAddresses[i])):
			#account for wheelbarro.ive ending
			tempending = ojbectEnding
			if (i == 2 and j == 5):
				tempending = '.ive'
			objectFiles[i].append(viz.add(commonAddress + objectAddresses[i][j] + tempending))
			objectFiles[i][j].visible(viz.OFF)

#check to see if subject is close to the arrow and cylinder
#EXPERIMENT
def update():
	global currentState, arrow, cylinder, view 
	global targetPosition
	if(currentState == 1 or currentState == 3):
		#see if the participant is close enough to the cylinder
		x = view.getPosition()[0] - targetPosition[0]
		y = view.getPosition()[2] - targetPosition[2]
		distSqrd = x*x + y*y
		radius = 1.2
		if(distSqrd <= radius):
			cylinder.color(0,1,0)
			#find the angle between the participant's view and the arrow
			#might have to add error in angle needed...
			pointA = view.getPosition()[0] + math.sin(math.radians(view.getEuler()[0] + ERROR)),0,view.getPosition()[2] + math.cos(math.radians(view.getEuler()[0] + ERROR))
			angle = get2Angle(view.getPosition(), pointA, arrow.getPosition())
			#angle += ERROR
			debug = False
			if debug:
				print "here is angle %d " %angle
				print "here is pointA",pointA
				print "here is the yaw %d", view.getEuler()[0]
			if(angle <= 10.0):
				arrow.color(0,1,0)
			else:
				arrow.color(1,0,0)
		else:
			cylinder.color(1,0,0)
			arrow.color(1,0,0)

	elif example:
		global exapmleCylinder
		x = view.getPosition()[0] - exapmleCylinder.getPosition()[0]
		y = view.getPosition()[2] - exapmleCylinder.getPosition()[2]
		distsqrd = x*x + y*y
		if distsqrd <= .8:
			exapmleCylinder.color(0,1,0)
		else:
			exapmleCylinder.color(1,0,0)
#a bunch of initialize things!
# PROBABLY SPLIT BETWEEN EXPERIMENT AND ENVIRONMENT...
FileReader()		
initializeObjectFiles()
initializeLocations()
getCurrentTestingLocationOrder()

debugInitialize = False
if debugInitialize:
	print targetLocations
	print targetObjects
example = False
keyEvent('e')
#rotate once
#keyEvent('r')	
view.setEuler(45,0,0)

#things to call all of the time
vizact.ontimer(1/30, checkStep)
vizact.ontimer(1, angleChangePerSecond)
vizact.ontimer(0.5, angleChangePerHalfSecond)
#update movement constantly
vizact.onupdate(0, moveNow)
#vizact.ontimer(0, checkOption1)
vizact.ontimer(0.2, update)
vizact.ontimer(0.2,checkTurning)
viz.callback(viz.KEYBOARD_EVENT, keyEvent)
print "outside of all ontimers"
