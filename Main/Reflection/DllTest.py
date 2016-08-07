import time
from ctypes import*

class Event(Structure):
    _fields_ = [("type", c_int),
				("data", c_int)]

VisionDll = windll.Vision

terminateVision = VisionDll.terminateVision
terminateVision.argtypes = [c_void_p]
terminateVision.restype = c_void_p

launchVision = VisionDll.launchVision
launchVision.argtypes = [c_bool, c_bool]
launchVision.restype = c_void_p

pollEvent = VisionDll.pollEvent
pollEvent.argtypes = [c_void_p,POINTER(Event)]
pollEvent.restype = c_int

Handle = launchVision(True, True)
print(Handle)
dat = Event(0,0)

Running = True

while Running:
	result = pollEvent(c_voidp(Handle),byref(dat))
	while result:
		print(result, " : ",dat.type," : ",dat.data)
		if dat.type == 4:
			Running = False
		result = pollEvent(c_voidp(Handle),byref(dat))
	time.sleep(1)

terminateVision(Handle)
