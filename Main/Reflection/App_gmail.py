from tkinter import*

import Cfg
from time import*

import wifsm2

class AppC_Gmail(Frame):
	def __init__(self, parent,X,Y):

	#### Initiate object variables
	# Variables for system operation
		self.Target_X = X
		self.Target_Y = Y
		self.Xmove=0
		self.Ymove=0
		self.speedy=2
		self.speedx=2
		self.name = "Gmail"
		self.hardheight = 320
		self.hardwidth = 502
		self.doomed = False

	# Class specific variables for object operation
		

	### End of variables

	### Execute startup code

			# Create frame for the app and place at given coordinates
		Frame.__init__(self, parent)
		Frame.config(self, bg="#000000")
		self.place(x=X, y=Y)

	
	### Draw the app
		
		response = wifsm2.emailList(Cfg.active_user, 5)
	
		image = PhotoImage(file = 'images\\gmail.gif')
		
		#Label(self, text = 'Gmail' , fg="white", bg="Black", font=("Helvetica", 16)).grid(row=0, column=1, columnspan=2, sticky=W)
		icon = Label(self, image=image, borderwidth=0, highlightthickness=0)
		icon.image = image
		icon.grid(row=0, column=0)
		
		row = 0
		for email in response:
			#name = ''.join(re.findall(r'<(.*?)>', email['From']))+":        "
			
			email['Date']=email['Date'][:-6]
			junk = email['From'].split("<")
			name = junk[0]
			Label(self, text=name , fg="white", bg="Black", font=("Helvetica", 12)).grid(row=1+(row*3), column=0, sticky=SW)
			Label(self, text=email["Subject"],anchor=W, justify=LEFT,wraplength=400,\
										 fg="white", bg="Black", font=("Helvetica", 12))\
										 .grid(row=1+(row*3), column=1, sticky=W, rowspan = 2)
	
			Label(self, text=email['Date'], fg="white", bg="Black", font=("Helvetica", 8)).grid(row=2+(row*3), column=0, sticky=NW)
			if row < 4:
				Frame(self, bg="White", height = 1, width = 500).grid(row=3+(row*3), column=0, sticky=NW, columnspan = 2)
			row = row + 1	
			
		
	### End of startup code

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

	def exfiltrate(self):
		if self.winfo_x() < Cfg.root.winfo_screenwidth()/2:
			self.Target_X = self.winfo_x()-32- 32-self.hardwidth
		else:
			self.Target_X = self.winfo_x() + 32 + 32 + self.hardwidth
		self.doomed = True

	def loophandler1000(self):
		#print(self.winfo_width(),self.winfo_height())
		pass

	def loophandler60000(self):
		pass
	

