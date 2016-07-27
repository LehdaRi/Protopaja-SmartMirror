from ctypes import*
import Cfg

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

dat = Event(0,0)

def StartVision():
	Cfg.vision = launchVision(True, True)

def CloseVision():
	Cfg.vision.terminateVision()

def ReadBuffer():
	Events = []
	result = pollEvent(c_voidp(Cfg.vision),byref(dat))
	while result:
		#print(result, " : ",dat.type," : ",dat.data)
		Events.append([dat.type,dat.data])
		result = pollEvent(c_voidp(Cfg.vision),byref(dat))
	return Events