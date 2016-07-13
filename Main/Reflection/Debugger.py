from tkinter import*

import AppControl
import User_Control
from Config import*

def DebugSwitch(event):	# Open or close the debugger window
	global debugger

	try:	# If Debugger window can be destroyed, do so...
		debugger.destroy()
		debugger = None

	except:	# Otherwise create the debugger window...

	# Create Toplevel window for the debugger
		debugger = Toplevel()
		debugger.title("Reflection Debugger")
		debugger.config(bg="#C0C0C0")
		debugger.bind("<F1>", DebugSwitch)

	# Create System Frame
		systemframe = LabelFrame(debugger, text="System")
		systemframe.pack( side = LEFT, fill = Y  )

			# Create background inverting button
		sfb_invert = Button(systemframe, text="Invert background", command=SysBgInvert)
		sfb_invert.pack( side = TOP, fill = X )
		sfb_newuser = Button(systemframe, text="New user", command=User_Control.UserCreate)
		sfb_newuser.pack( side = TOP, fill = X )
		sfb_login = Button(systemframe, text="Log in user", command=User_Control.UserLogIn)
		sfb_login.pack( side = TOP, fill = X )

	# Create Task Controller
		moveframe = LabelFrame(debugger, text="Move app")
		moveframe.pack( side = LEFT, fill = Y   )

			# Create place buttons
		cfb_NW = Button(moveframe, text = "NW" , command = lambda: App_Move(NW))
		cfb_NW.grid( row = 0, column = 0 , ipadx=2 )
		cfb_W = Button(moveframe, text = "W" , command = lambda: App_Move(W))
		cfb_W.grid( row = 1, column = 0 , ipadx=6 )
		cfb_SW = Button(moveframe, text = "SW" , command = lambda: App_Move(SW))
		cfb_SW.grid( row = 2, column = 0 , ipadx=4 )
		cfb_NE = Button(moveframe, text = "NE" , command = lambda: App_Move(NE))
		cfb_NE.grid( row = 0, column = 1 , ipadx=4 )
		cfb_E = Button(moveframe, text = "E" , command = lambda: App_Move(E))
		cfb_E.grid( row = 1, column = 1 , ipadx=9 )
		cfb_SE = Button(moveframe, text = "SE" , command = lambda: App_Move(SE))
		cfb_SE.grid( row = 2, column = 1 , ipadx=6 )

	# Create Task Manager
		taskframe = LabelFrame(debugger, text="Task manager")
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
		debugger.lift()



def Fill_Manager(taskbox):
	global app_list
	
	for i in app_list:
		taskbox.insert(END, i.name)


def App_Move(target):
	pass


def SysBgInvert():
	pass
	
def Task_New():
	global apps

	RunWin = Toplevel()
	RunButtons = []

	for i in apps:
		print(i)
		RunButtons.append(Button(RunWin, text=i, command = lambda i=i: AppControl.Place_App(i,32,32)))
		RunButtons[-1].pack(side = TOP, fill = X)




def Task_Close(task):
	task.destroy()
	

def DebugClose():	# Close the Debugger window
	global debugger

	debugger.destroy()
	debugger = None

def DebugAppBlack():
	global app_list

#	app_list[0].AppBGBlack()
	for i in app_list:
		i.AppBGBlack()

def DebugAppBlack():
	global app_list

#	app_list[0].AppBGWhite()
	for i in app_list:
		i.AppBGWhite()

