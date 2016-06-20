import viz
import vizact
import sys
import os
sys.path.append(os.path.join('C:\Users\Bryton\Downloads\myo-python-master'))
sys.path.append(os.path.join('C:\Users\Bryton\Downloads\myo-sdk-win-0.8.1'))
import myo
from myo.lowlevel import pose_t, stream_emg
import math
from myo.six import print_
import random
import oculus

viz.setMultiSample(4)
viz.go()


dojo = viz.add('piazza.osgb')
sky = viz.add('sky_day.osgb')

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

	def on_orientation_data(self, myo, timestamp, orientation):
		x = 2

	def on_accelerometor_data(self, myo, timestamp, acceleration):
		print(acceleration)

	def on_gyroscope_data(self, myo, timestamp, gyroscope):
		x = 1

	def on_unlock(self, myo, timestamp):
		print_('unlocked')

	def on_lock(self, myo, timestamp):
		print_('locked')

	def on_sync(self, myo, timestamp, arm, x_direction):
		print_('synced', arm, x_direction)
		

	def on_unsync(self, myo, timestamp):
		print_('unsynced')
		

def main():
	hub = myo.Hub()
	hub.set_locking_policy(myo.locking_policy.none)
	hub.run(1000, Listener())
	
