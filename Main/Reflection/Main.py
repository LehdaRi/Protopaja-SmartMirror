from tkinter import*

from Config import*

import App_Time
from GUI import*
import Debugger




def Main():
	global root

	root = GUIC()
	# Bind keyboard keys.
	root.bind("<F1>", Debugger.DebugSwitch)	# Bind F1 Used for debugger window swiching
	root.grid()


# Start delayed loops
	root.after(40, LoopHandler40)
	root.after(1000, LoopHandler1000)
	root.after(60000, LoopHandler60000)
	root.mainloop()

def LoopHandler40():
	for i in app_list:
		i.loophandler40()
	root.after(40, LoopHandler40)
	
def LoopHandler1000():
	for i in app_list:
		i.loophandler1000()
	root.after(1000, LoopHandler1000)	
	
def LoopHandler60000():
	for i in app_list:
		i.loophandler60000()
	root.after(60000, LoopHandler60000)	
	
			

Main()