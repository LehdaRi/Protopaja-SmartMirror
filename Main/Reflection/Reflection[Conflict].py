from tkinter import *
from App_Time import*
from Debugger import*

class GUIO(Tk):
	def __init__(self, *args, **kwargs):
		
		Tk.__init__(self, *args, **kwargs)
		self.geometry('%dx%d+%d+%d' % (self.winfo_screenwidth(), self.winfo_screenheight(), 0, 0))
		#self.attributes('-fullscreen', True)
		self.config(bg="#000000")
		self.ObjectList = []
		self.ObjectList.append(App_Time(self,100,100))
		self.ObjectList.append(App_Time(self,300,100))

		self.Debugger = Toplevel()


		

def Main():
	root = GUIO()

	root.mainloop()

Main()
