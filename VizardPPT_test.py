import viz
import vizinput
import vizact
import win32pipe
import sys

viz.go()

vrpn = viz.add('vrpn7.dle')
#Check the name of your PPT machine and change the name in the line below if necessary
tracker = vrpn.addTracker('PPT0@10.10.37.178',0)
print(tracker.getVerbose);

if tracker.valid():
     vizinput.message('Connection established to PPT marker 1')
else:
     vizinput.message('Failed to detect PPT marker 1')






def printPos():
	print(tracker.getPosition());


def pipeRefresh(p):
	print("check1")
	buf = str(tracker.getPosition()[0]) + "-" + str(tracker.getPosition()[1]) + "-" + str(tracker.getPosition()[2])
	print(sys.getsizeof(buf))
	print("check2")
	print (p)
	p = win32pipe.CallNamedPipe(
		r'\\.\pipe\Demo',
		"hello",
		65536,
		win32pipe.NMPWAIT_NOWAIT)
	print("check3")

def main():
	print(sys.version_info);
	#vizact.ontimer(0, printPos);
	p = win32pipe.CreateNamedPipe(
		r'\\.\pipe\Demo',
		win32pipe.PIPE_ACCESS_DUPLEX,
		win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
		1,
		65536,
		65536,
		300,
		None)
	print("pre connect")
	#win32pipe.ConnectNamedPipe(p, None)
	print("post connect")





	#vizact.ontimer(0, printPos)
	vizact.ontimer(1, pipeRefresh, p)

def fileJunk():
    index = 0
    filePath = os.path.join('Z:\\Desktop\\New Unity Project', 'coordinates.txt')
    while (index < 100000):
        try:
            f = open(filePath, 'wb')
            f.seek(0)
            f.truncate()
            f.write(str(index).encode())
            index += 1
            print('loop # ', index, '\n')
            f.close()
            time.sleep(.01)
        except:
            pass

main()
