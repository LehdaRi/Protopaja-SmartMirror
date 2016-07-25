from tkinter import*

import Cfg
from time import*


class AppC_Time(Frame):
	def __init__(self, parent,X,Y):

	#### Initiate object variables
	# Variables for system operation
		self.Target_X = X
		self.Target_Y = Y
		self.Xmove=0
		self.Ymove=0
		self.speedy=2
		self.speedx=2
		self.name = "Clock"
		self.hardheight = 138
		self.hardwidth = 168
		

	# Class specific variables for object operation
			# Create current time list
		self.daylist = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
		self.timestringlist = []
		self.timelist = [StringVar(), StringVar(), StringVar()]

			# Initial values for time
		self.timestringlist = localtime(time())
		self.timelist[0].set("{:d}:{:d}".format(self.timestringlist[3],self.timestringlist[4]))
		self.timelist[1].set(self.daylist[self.timestringlist[6]])
		self.timelist[2].set("{:02d}.{:02d}.{:d}".format(self.timestringlist[2],self.timestringlist[1],self.timestringlist[0]))
		
	### End of variables

	### Execute startup code

			# Create frame for the app and place at given coordinates
		Frame.__init__(self, parent)
		Frame.config(self, bg="#000000")
		self.place(x=X, y=Y)

	
	### Draw the app

		# Create and fill labels to display text
		timelabel = Label(self, textvariable=self.timelist[0], fg="white", bg = "black", font=("Helvetica", 48))
		timelabel.pack()
		datelabel = Label(self, textvariable=self.timelist[2], fg="white", bg = "black", font=("Helvetica", 16))
		datelabel.pack()
		daylabel = Label(self, textvariable=self.timelist[1], fg="white", bg = "black", font=("Helvetica", 16))
		daylabel.pack()	


	### End of startup code

	def loophandler40(self):
		self.timestringlist = localtime(time())
		self.timelist[0].set("{:02d}:{:02d}".format(self.timestringlist[3],self.timestringlist[4],))
		self.timelist[1].set(self.daylist[self.timestringlist[6]])
		self.timelist[2].set("{:02d}.{:02d}.{:d}".format(self.timestringlist[2],self.timestringlist[1],self.timestringlist[0]))
		
	### Move animation
		self.speedy = abs(self.Target_Y - self.winfo_y())/10
		self.speedx = abs(self.Target_X - self.winfo_x())/10

		if abs(self.Target_Y - self.winfo_y()) <= 2:
			self.speedy = abs(self.Target_Y - self.winfo_y())

		if abs(self.Target_X - self.winfo_x()) <= 2:
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




	def loophandler1000(self):
		pass

	def loophandler60000(self):
		pass
	

