from tkinter import*

import AppControl
import User_Control
import Cfg

def DebugSwitch(event):	# Open or close the debugger window

	try:	# If Debugger window can be destroyed, do so...
		Cfg.debugger.destroy()
		Cfg.debugger = None

	except:	# Otherwise create the debugger window...

	# Create Toplevel window for the debugger
		Cfg.debugger = Toplevel()
		Cfg.debugger.title("Reflection Debugger")
		Cfg.debugger.config(bg="#C0C0C0")
		Cfg.debugger.bind("<F1>", DebugSwitch)

	# Create System Frame
		systemframe = LabelFrame(Cfg.debugger, text="System")
		systemframe.pack( side = LEFT, fill = Y  )

			# Create background inverting button
		sfb_invert = Button(systemframe, text="Invert background", command=SysBgInvert)
		sfb_invert.pack( side = TOP, fill = X )
		sfb_newuser = Button(systemframe, text="New user", command=User_Control.UserCreate)
		sfb_newuser.pack( side = TOP, fill = X )
		sfb_login = Button(systemframe, text="Log in user", command=User_Control.UserLogIn)
		sfb_login.pack( side = TOP, fill = X )

	# Create Task Controller
		moveframe = LabelFrame(Cfg.debugger, text="Move app")
		moveframe.pack( side = LEFT, fill = Y   )

			# Create place buttons
		cfb_NW = Button(moveframe, text = "NW" , command = lambda: AppControl.App_Move(app_list[taskbox.index(ACTIVE)],NW))
		cfb_NW.grid( row = 0, column = 0 , ipadx=2 )
		cfb_W = Button(moveframe, text = "W" , command = lambda: AppControl.App_Move(app_list[taskbox.index(ACTIVE)],W))
		cfb_W.grid( row = 1, column = 0 , ipadx=6 )
		cfb_SW = Button(moveframe, text = "SW" , command = lambda: AppControl.App_Move(app_list[taskbox.index(ACTIVE)],SW))
		cfb_SW.grid( row = 2, column = 0 , ipadx=4 )
		cfb_NE = Button(moveframe, text = "NE" , command = lambda: AppControl.App_Move(app_list[taskbox.index(ACTIVE)],NE))
		cfb_NE.grid( row = 0, column = 1 , ipadx=4 )
		cfb_E = Button(moveframe, text = "E" , command = lambda: AppControl.App_Move(app_list[taskbox.index(ACTIVE)],E))
		cfb_E.grid( row = 1, column = 1 , ipadx=9 )
		cfb_SE = Button(moveframe, text = "SE" , command = lambda: AppControl.App_Move(app_list[taskbox.index(ACTIVE)],SE))
		cfb_SE.grid( row = 2, column = 1 , ipadx=6 )

	# Create Task Manager
		taskframe = LabelFrame(Cfg.debugger, text="Task manager")
		taskframe.pack( side = LEFT, fill = Y  )

			 # Create new task button
		tfb_new = Button(taskframe, text="Run...", command = Task_New )
		tfb_new.pack( side = TOP, fill = X )

			# Create open tasks listbox
		taskbox = Listbox(taskframe)
		taskbox.pack(side = TOP)
		Fill_Manager(taskbox)

			# Create close task button
		tfb_close = Button(taskframe, text="Close task", command = lambda: Task_Close(app_list[taskbox.index(ACTIVE)]) )
		tfb_close.pack( side = TOP, fill = X )

	# Make sure that the debugger is in the front
		Cfg.debugger.lift()



def Fill_Manager(taskbox):
	
	for i in Cfg.app_list:
		taskbox.insert(END, i.name)


def App_Move(target):
	pass


def SysBgInvert():
	pass
	
def Task_New():


	RunWin = Toplevel()

	appsbox = Listbox(RunWin)
	appsbox.pack(side = LEFT)
	for i in Cfg.apps:
		appsbox.insert(END, i)

	placeframe = Frame(RunWin)
	placeframe.pack(side = LEFT)
	placeNE = Button(placeframe, text="NE", command = lambda: AppControl.Place_App_Corner(Cfg.apps[appsbox.index(ACTIVE)],"NE"))
	placeSE = Button(placeframe, text="SE", command = lambda: AppControl.Place_App_Corner(Cfg.apps[appsbox.index(ACTIVE)],"SE"))
	placeSW = Button(placeframe, text="SW", command = lambda: AppControl.Place_App_Corner(Cfg.apps[appsbox.index(ACTIVE)],"SW"))
	placeNS = Button(placeframe, text="NW", command = lambda: AppControl.Place_App_Corner(Cfg.apps[appsbox.index(ACTIVE)],"NW"))
	
	placeNE.grid(row = 0, column = 1, ipadx=3)
	placeSE.grid(row = 1, column = 1, ipadx=5)
	placeSW.grid(row = 1, column = 0, ipadx=3)
	placeNS.grid(row = 0, column = 0, ipadx=4)




def Task_Close(task):
	task.destroy()
	

def DebugClose():	# Close the Debugger window

	Cfg.debugger.destroy()
	Cfg.debugger = None

def DebugAppBlack():

#	app_list[0].AppBGBlack()
	for i in Cfg.app_list:
		i.AppBGBlack()

def DebugAppBlack():

#	app_list[0].AppBGWhite()
	for i in Cfg.app_list:
		i.AppBGWhite()

