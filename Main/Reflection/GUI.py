from tkinter import*

from Config import*

from App_Time import*

class GUIC(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

			# Configure background window
		self.geometry('%dx%d+%d+%d' % (self.winfo_screenwidth(), self.winfo_screenheight(), 0, 0))
		self.attributes('-fullscreen', True)
		self.config(bg="#000000")


