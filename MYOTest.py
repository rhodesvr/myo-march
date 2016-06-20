'''import os, sys, viz, vizact
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

avgP = {}
def avgPrint(v, n, id):
	if not (id in avgP):
		avgP[id] = []
	avgP[id].append(v)
	if (len(avgP[id]) > n):
		avgP[id].pop(0)
	print id + ": " + str(sum(avgP[id]) / len(avgP[id]))
		
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
		#print "Event", event
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
			''or1x[0] = orx[0]
			or1y[0] = ory[0]
			or1z[0] = orz[0]
			or1w[0] = orw[0]''
			#myo.set_stream_emg(stream_emg.enabled)
		elif pose == pose_t.fingers_spread:
			egg = 0
			#print_("=" * 80)
			#myo.set_stream_emg(stream_emg.disabled)

	def on_orientation_data(self, myo, timestamp, orientation):
		print "Ori", orientation
		#show_output('orientation', orientation)
		#print_(orientation) #- The actual orientation quaternion that seems to be from -1 to 1
		#print_(orientation[0])
		''orx[0] = orientation[0]
		ory[0] = orientation[1]
		orz[0] = orientation[2]
		orw[0] = orientation[3]
		if (or1x[0] == [0] and or1y[0] == [0] and or1z[0] == 0 and or1w[0] == [0]):
			or1x[0] = orientation[0]
			or1y[0] = orientation[1]
			or1z[0] = orientation[2]
			or1w[0] = orientation[3]''

	def on_accelerometor_data(self, myo, timestamp, acceleration):
		print "Acceleration", acceleration
		#avgPrint(acceleration[0], 10, "Acceleration X")
		x = 4
	def on_gyroscope_data(self, myo, timestamp, gyroscope):
		print "\nGyro", gyroscope
		#show_output('gyroscope', gyroscope)
		''gy[0] = gyroscope[0]
		gy2[0] = gyroscope[1]
		gy3[0] = gyroscope[2]''
			

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

def main():
	myo.init()
	hub = myo.Hub()
	hub.set_locking_policy(myo.locking_policy.none)
	hub.run(1000, Listener())
	vizact.onkeydown('p', hub.shutdown)
	#x = raw_input()
	#hub.shutdown()
main()'''
import vizmat
#import numpy as np
import vizmatplotlib.pyplot as plt
import vizmatplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)        # x-array
line, = ax.plot(x, np.sin(x))

def animate(i):
    line.set_ydata(np.sin(x+i/10.0))  # update the data
    return line,

#Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
    interval=25, blit=True)
plt.show()