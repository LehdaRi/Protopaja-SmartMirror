from tkinter import*
from ctypes import*

import Cfg
import Cursor
import User_Control
import Debugger
import AppControl
import dllhandler
import wifsm2
import random
### Dll startup




def Main():
	dllhandler.StartVision()

	### Initiate
	Cfg.root = Tk()
	Cfg.root.geometry('%dx%d+%d+%d' % (Cfg.root.winfo_screenwidth(), Cfg.root.winfo_screenheight(), 0, 0))
	Cfg.root.attributes('-fullscreen', True)
	Cfg.root.config(bg="#000000")
	# Bind keyboard keys.
	Cfg.root.bind("<F1>", Debugger.DebugSwitch)	# Bind F1 Used for debugger window swiching
	Cfg.root.grid()


# Start delayed loops
	Cfg.root.after(40, LoopHandler40)
	Cfg.root.after(1000, LoopHandler1000)
	Cfg.root.after(60000, LoopHandler60000)
	Cfg.root.after(1000, AppControl.Open_User_Apps)
	Cfg.root.mainloop()



def LoopHandler40():
	for i in Cfg.app_list:
		i.loophandler40()

	for i in range(len(Cfg.app_list)):
		
		if Cfg.app_list[i].Xmove==0 and Cfg.app_list[i].Ymove==0 and Cfg.app_list[i].doomed == True:
			Cfg.app_list[i].destroy()
			Cfg.app_list[i] = None
			
	AppControl.App_List_Reorganize()
	
	
	Cfg.root.after(16, LoopHandler40)
	
	### Event Handler
	Cfg.Events = dllhandler.ReadBuffer()
	if Cfg.Events:
		print(Cfg.Events)
	EventsHandler()
	try:
		Cfg.cursor.Draw()
	except:
		pass
	
	
def LoopHandler1000():
	for i in Cfg.app_list:
		i.loophandler1000()
	Cfg.root.after(5000, LoopHandler1000)	
	
	
def LoopHandler60000():
	for i in Cfg.app_list:
		i.loophandler60000()
	Cfg.root.after(60000, LoopHandler60000)	
	
def EventsHandler():
	userin = None
	users = [None,"Dummy","Dumbo","Axel"]


	for event in Cfg.Events:
		if event[0] == 1:
			if event[1] == 0:
				userin = "Default"
			elif event[1] == 5:
				userin = users[random.randint(1,3)]
		elif event[0] == 2:
			if event[1] == 0:
				userin = "Default"
			elif event[1] == 5:
				userin = "Default"

	if not userin == Cfg.active_user:
		Cfg.active_user = userin
		AppControl.Reload_Apps()

	"""for event in Cfg.Events:
		if event[0] == 1:
			userin = users[event[1]]
		elif event[0] == 2:
			userout = users[event[1]]
	if not userout == None and userin == None:
		if userout == Cfg.active_user:
			Cfg.active_user = "Default"
			AppControl.Reload_Apps()

	if not userin == None:
		Cfg.active_user = userin
		AppControl.Reload_Apps()"""


Main()