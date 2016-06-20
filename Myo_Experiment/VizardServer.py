'''
We are foregoing this approach as it has continued to prove difficult.
Instead, we will pursue Ansel's approach of actual file i/o
'''

import time
import struct
import viz, vizinput, vizact
import os


viz.go()

vrpn = viz.add('vrpn7.dle')
#Check the name of your PPT machine and change the name in the line below if necessary
tracker = vrpn.addTracker('PPT0@WORLDVIZ-PC',0)
print(tracker.getVerbose);

if tracker.valid():
    vizinput.message('Connection established to PPT marker 1')
else:
    vizinput.message('Failed to detect PPT marker 1')


print("about to start while loop")

filePath = os.path.join(os.getcwd(), 'coordinates.txt')


def io():
	try:
		f = open(filePath, 'wb')
		f.seek(0)
		f.truncate()
		position = tracker.getPosition()
				
		s = str(position[0]) + "," + str(position[1]) + "," + str(position[2])
		
		f.write(s.encode())
		f.close()
		#print("just wrote", s)
		time.sleep(.01)
	except:
		pass

def p():
	print(tracker.getPosition())

def main():
	vizact.ontimer(0, io)
	vizact.ontimer(0, p)
			
main()
