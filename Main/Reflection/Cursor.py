import Cfg
from tkinter import*

class Cursor(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		Frame.config(self, bg="#000000")
		self.pack()

		self.TargetApp = Cfg.app_list[0]
		self.gif = [PhotoImage(file = "images/arrow_left.gif"), \
						PhotoImage(file = "images/arrow_right.gif")]

	# Variables for animation
		self.cursor = None
		
	# Variables for movement
		if (self.TargetApp.winfo_x() < Cfg.root.winfo_screenwidth()/2):
			self.Target_X = self.TargetApp.winfo_x()+self.TargetApp.winfo_width()+32
		else:
			self.Target_X = self.TargetApp.winfo_x()-32-100
		self.Target_Y = self.TargetApp.winfo_y()	
		self.Xmove=0
		self.Ymove=0
		self.speedy=2
		self.speedx=2
		self.frame = 0
		self.seek_x = 0
		self.seek_y = 0

		self.slaveframe = Frame(self)
		self.slaveframe.pack()
		self.cursor = Label(self.slaveframe, image = self.gif[self.frame], bg="#000000")
		self.cursor.pack()

### Move cursor function

	def CursorMoveUp(self):
		best = self.TargetApp
		for i in Cfg.app_list:
			if not i == self.TargetApp:
				if self.winfo_y() > i.winfo_y() and \
						(best == self.TargetApp or best.winfo_y() < i.winfo_y()) and \
						((self.winfo_x() < Cfg.root.winfo_screenwidth()/2 and \
						i.winfo_x() < Cfg.root.winfo_screenwidth()/2) or \
						(self.winfo_x() > Cfg.root.winfo_screenwidth()/2 and \
						i.winfo_x() > Cfg.root.winfo_screenwidth()/2)):
					print("Found")
					best = i
						
				else:
					print("Not Found")
			else:
				print("Self")
		self.TargetApp = best
		if (self.TargetApp.winfo_x() < Cfg.root.winfo_screenwidth()/2):
			print("LEFT")
			self.Target_X = self.TargetApp.winfo_x()+self.TargetApp.winfo_width()+32
		else:
			print("RIGHT")
			self.Target_X = self.TargetApp.winfo_x()-32-100
		self.Target_Y = self.TargetApp.winfo_y()
		
		
	def CursorMoveDown(self):
		best = self.TargetApp
		for i in Cfg.app_list:
			if not i == self.TargetApp:
				if self.winfo_y() < i.winfo_y() and \
						(best == self.TargetApp or best.winfo_y() > i.winfo_y()) and \
						((self.winfo_x() < Cfg.root.winfo_screenwidth()/2 and \
						i.winfo_x() < Cfg.root.winfo_screenwidth()/2) or \
						(self.winfo_x() > Cfg.root.winfo_screenwidth()/2 and \
						i.winfo_x() > Cfg.root.winfo_screenwidth()/2)):
					print("Found")
					best = i
						
				else:
					print("Not Found")
			else:
				print("Self")
		self.TargetApp = best
		if (self.TargetApp.winfo_x() < Cfg.root.winfo_screenwidth()/2):
			self.Target_X = self.TargetApp.winfo_x()+self.TargetApp.winfo_width()+32
		else:
			self.Target_X = self.TargetApp.winfo_x()-32-100
		self.Target_Y = self.TargetApp.winfo_y()

	def CursorMoveLeft(self):
		best = self.TargetApp
		for i in Cfg.app_list:
			if not i == self.TargetApp or not self.winfo_x() < Cfg.root.winfo_screenwidth()/2:
				if i.winfo_x() < Cfg.root.winfo_screenwidth()/2:
					if best == self.TargetApp:
						best = i
					elif abs(best.winfo_y()-self.winfo_y()) > abs(i.winfo_y()-self.winfo_y()):
						best = i
		self.TargetApp = best
		if (self.TargetApp.winfo_x() < Cfg.root.winfo_screenwidth()/2):
			self.Target_X = self.TargetApp.winfo_x()+self.TargetApp.winfo_width()+32
		else:
			self.Target_X = self.TargetApp.winfo_x()-32-100
		self.Target_Y = self.TargetApp.winfo_y()
	
	def CursorMoveRight(self):
		best = self.TargetApp
		for i in Cfg.app_list:
			if not i == self.TargetApp or not self.winfo_x() > Cfg.root.winfo_screenwidth()/2:
				if i.winfo_x() > Cfg.root.winfo_screenwidth()/2:
					if best == self.TargetApp:
						best = i
					elif abs(best.winfo_y()-self.winfo_y()) > abs(i.winfo_y()-self.winfo_y()):
						best = i
		self.TargetApp = best
		if (self.TargetApp.winfo_x() < Cfg.root.winfo_screenwidth()/2):
			self.Target_X = self.TargetApp.winfo_x()+self.TargetApp.winfo_width()+32
		else:
			self.Target_X = self.TargetApp.winfo_x()-32-100
		self.Target_Y = self.TargetApp.winfo_y()


### Draw image function

	def Draw(self):
		if not (self.winfo_x() == self.Target_X) or not \
			(self.winfo_y() == self.Target_Y):
			
			if ((self.TargetApp.winfo_x() < Cfg.root.winfo_screenwidth()/2) and self.frame == 1):
				self.frame = 0
				self.slaveframe.destroy()
				self.slaveframe = None
				self.cursor = None
				self.slaveframe = Frame(self)
				self.slaveframe.pack()
				self.cursor = Label(self.slaveframe, image = self.gif[self.frame], bg="#000000")
				self.cursor.pack()
			elif ((self.TargetApp.winfo_x() > Cfg.root.winfo_screenwidth()/2) and self.frame == 0):
				self.frame = 1
				self.slaveframe.destroy()
				self.slaveframe = None
				self.cursor = None
				self.slaveframe = Frame(self)
				self.slaveframe.pack()
				self.cursor = Label(self.slaveframe, image = self.gif[self.frame], bg="#000000")
				self.cursor.pack()
		
		

			self.speedy = abs(self.Target_Y - self.winfo_y())/10
			self.speedx = abs(self.Target_X - self.winfo_x())/10

			if abs(self.Target_Y - self.winfo_y()) <= 5:
				self.speedy = abs(self.Target_Y - self.winfo_y())

			if abs(self.Target_X - self.winfo_x()) <= 5:
				self.speedx = abs(self.Target_X - self.winfo_x())

			if self.Target_X < self.winfo_x():
				self.Xmove=-self.speedx
			elif self.Target_X > self.winfo_x():
				self.Xmove=self.speedx
			elif self.Target_X == self.winfo_x():
				self.Xmove=0

			if self.Target_Y < self.winfo_y():
				self.Ymove=-self.speedy
			elif self.Target_Y > self.winfo_y():
				self.Ymove=self.speedy
			elif self.Target_Y == self.winfo_y():
				self.Ymove=0


			self.place(x=self.winfo_x()+self.Xmove,y=self.winfo_y()+self.Ymove)

	
def CursorMove(dir):
	if dir == "UP":
		Cfg.cursor.CursorMoveUp()
	elif dir == "DOWN":
		Cfg.cursor.CursorMoveDown()
	elif dir == "LEFT":
		Cfg.cursor.CursorMoveLeft()
	elif dir == "RIGHT":
		Cfg.cursor.CursorMoveRight()


def CursorOn():
	if len(Cfg.app_list) > 0:
		
		Cfg.cursor = Cursor(Cfg.root)

def CursorOff():
	try:
		Cfg.cursor.destroy()
		Cfg.cursor = None
	except:
		pass