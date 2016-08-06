from tkinter import*

import wifsm2
import Cfg
import copy
from time import*


class AppC_Ruokalista(Frame):
	def __init__(self, parent,X,Y):

	#### Initiate object variables
	# Variables for system operation
		self.Target_X = X
		self.Target_Y = Y
		self.Xmove=0
		self.Ymove=0
		self.speedy=2
		self.speedx=2
		self.name = "Ruokalista"
		self.hardheight = 138
		self.hardwidth = 168
		self.doomed = False
		self.foodlist = wifsm2.getRuokalistat()
	# Class specific variables for object operation
		self.divider=[]
		self.names = []
		self.foods = []
		self.active = 0
	### End of variables

	### Execute startup code

			# Create frame for the app and place at given coordinates
		Frame.__init__(self, parent)
		Frame.config(self, bg="#000000")
		self.place(x=X, y=Y)

	
	### Draw the app
		self.divider.append(Frame(self, bg="White", height = 3, width = 250))
		self.divider[-1].pack()

		self.Title = Label(self, text = "RUOKALISTA", fg="white", bg="Black", font=("Helvetica", 16))
		self.Title.pack(anchor=W)
		
		self.divider.append(Frame(self, bg="White", height = 3, width = 250))
		self.divider[-1].pack()

		for keys,values in self.foodlist.items():
			if values:
				self.names.append(Label(self, text = keys, fg="white", bg="Black", font=("Helvetica", 16)))
				junk = []
				for i in values:
					junk.append(Label(self, text = i,anchor=W, justify=LEFT,wraplength= 250, fg="white", bg="Black", font=("Helvetica", 10)))
				self.foods.append(junk)

		self.names[0].pack()
		for i in self.foods[0]:
			i.pack(anchor=W)

	### End of startup code
	def exfiltrate(self):
		if self.winfo_x() < Cfg.root.winfo_screenwidth()/2:
			self.Target_X = self.winfo_x() - 32 - 32-self.hardwidth
		else:
			self.Target_X = self.winfo_x() + 32 + 32 + self.hardwidth
		self.doomed = True

	def loophandler40(self):
		


		### Move animation handling below ###
		self.Target_Y = int(self.Target_Y)
		self.Target_X = int(self.Target_X)
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
		### Move animation above this line ###


	def loophandler1000(self):

		self.names[self.active].pack_forget()
		for i in self.foods[self.active]:
			i.pack_forget()


		if self.active == len(self.names)-1:
			self.active = 0
		else:
			self.active += 1


		self.names[self.active].pack(anchor=W)
		for i in self.foods[self.active]:
			i.pack(anchor=W)

	def loophandler60000(self):
		pass
	

