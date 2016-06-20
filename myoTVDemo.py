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


viz.setMultiSample(4)
viz.go()
viz.phys.enable()
viz.phys.setGravity(0,0,0)
dojo = viz.add('dojo.osgb')
#dojo.setScale([20,0,20])
#frame = viz.add("frame.dae")
sky = viz.add('sky_day.osgb')


player_matrix = viz.Matrix()
targetMachine = 'PC-SANDERS1'
targetMailbox = viz.addNetwork(targetMachine)

def sendPosition():
	#Retrieve current transform of viewpoint	
	mat = viz.MainView.getMatrix()

	#Send position/rotation to target network object
	targetMailbox.send(action=updatePlayer, quat=mat.getQuat(), pos=mat.getPosition())

# Start a timer that sends out data over the network every frame
vizact.ontimer(0,sendPosition)


def updatePlayer(e):
	player_matrix.setPosition(e.pos)
	player_matrix.setQuat(e.quat)

# Listens for any incomming messages
def onNetwork(e):
	if e.sender.upper() == targetMachine:
		e.action(e)

# Register network to listen from incomming messages
viz.callback(viz.NETWORK_EVENT, onNetwork)


#-----------------
#-Main-View-Setup-
#-----------------

testsCompleted = 0 # amount of rounds completed, condition changes if 15 are completed
view = viz.MainView
view.collisionBuffer(1.8)
c = [0.0]

viz.collision(viz.ON)
ori = oculus.Rift()
global navigationNode
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)
viewLink.preMultLinkable(ori.getSensor())


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
# Setup Oculus Rift ori
"""ori = oculus.Rift()
if not ori.getSensor():
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
      
    navigationNode.setPosition(math.cos(ori.getSensor().getEuler()[0]*pi/180-90)*c[0],0,-math.sin(ori.getSensor().getEuler()[0]*pi/180-90)*c[0], viz.REL_PARENT)
    '''
        print(ori.getSensor().getEuler())
        #move(0,0,c[0])
    else:
        c[0] = -1*(prev-winglE[1])/100
      
        #move(0,0,c[0])
        navigationNode.setPosition(math.sin(ori.getSensor().getEuler()[0])*c[0],0,math.sin(ori.getSensor().getEuler()[0])*c[0], viz.REL_PARENT)'''
    #print(math.cos(joel[0]) , " " , math.sin(joel[0]))
    #print(joel[0])
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

    def on_event(self, kind, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, kind, event):
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
    viz.setMultiSample(4)
    viz.fov(150)
    wingl = viz.addChild('basketball.osgb')
    wingl.setScale([10,0.3,1])
    wingl.setCenter([100,100,100])
    wingl.setEuler([0,90,0])
    wingl.collideSphere(0.5)
    lStartPOS = [ 0, 2.5, 2 ]
    wingl.setPosition( lStartPOS )
    wingr = viz.addChild('basketball.osgb')
    wingr.setScale([10,0.3,1])
    wingr.setCenter([100,100,100])
    wingr.setEuler([0,90,0])
    wingr.collideSphere(0.5)
    rStartPOS = [ 0, 2.5, 2 ]
    wingr.setPosition( rStartPOS )

    #viz.MainView.setPosition([0,2,-15])
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    hub.run(1000, Listener())
    vizact.ontimer(0.01 ,updateMyo, [gy, gy2, gy3, wingl, orx, ory, orz, orw, or1x, or1y, or1z, or1w, wingr])

main()