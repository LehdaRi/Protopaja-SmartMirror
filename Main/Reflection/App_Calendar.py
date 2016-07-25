from tkinter import*

import Cfg

import wifsm2

class AppC_Calendar(Frame):
	def __init__(self, parent,X,Y):

	#### Initiate object variables
	# Variables for system operation
		self.name = "Calendar"
		self.Target_X = X
		self.Target_Y = Y
		self.Xmove=0
		self.Ymove=0
		self.speedy=2
		self.speedx=2
		self.hardheight = 138
		self.hardwidth = 168

	# Class specific variables for object operation

			# Get calendar entries
		print(Cfg.active_user)
		self.events = wifsm2.calendarList(Cfg.active_user)
		print(self.events)
		self.divider=[]
		self.CalendarEntries=[]
		self.CalendarTimes=[]
		self.StartTimes=[]
		self.EndTimes=[]
		self.Title=[]
		
	### End of variables

	### Execute startup code

			# Create frame for the app and place at given coordinates
		Frame.__init__(self, parent)
		Frame.config(self, bg="#000000")
		self.place(x=X, y=Y)
		
			# Create and fill labels to display text
		self.title = Label(self, text = "Upcoming Events", fg="white", bg="Black", font=("Helvetica", 16))
		self.title.pack()
		self.divider.append(Frame(self, bg="White", height = 3, width = 200))
		self.divider[-1].pack()
		for i in self.events:
			junk = i["start"]
		# Create frame to hold the calendar entry
			self.CalendarEntries.append(Frame(self, bg="Black"))
			self.CalendarEntries[-1].pack()
				# Create label with the date
			self.CalendarTimes.append(Label(self.CalendarEntries[-1], text = junk[2]+"."+junk[1]+"."+junk[0], fg="white", bg = "black", font=("Helvetica", 12)))
			self.CalendarTimes[-1].grid(row=0, columnspan=2, sticky=W)
				# Create a divider line
			self.divider.append(Frame(self.CalendarEntries[-1], bg="White", height = 1, width = 200))
			self.divider[-1].grid(row=1, columnspan=2)
				# Create label with the start time
			self.StartTimes.append(Label(self.CalendarEntries[-1], text = junk[3]+":"+junk[4], fg="white", bg = "black", font=("Helvetica", 12)))
			self.StartTimes[-1].grid(row=2,column=0,sticky=W)

			junk = i["end"]
				# Create label with the end time
			self.StartTimes.append(Label(self.CalendarEntries[-1], text = junk[3]+":"+junk[4], fg="white", bg = "black", font=("Helvetica", 12)))
			self.StartTimes[-1].grid(row=3,column=0,sticky=W)
				# Create label with the name of the event
			self.Title.append(Label(self.CalendarEntries[-1], text = i["title"], fg="white", bg = "black", font=("Helvetica", 12)))
			self.Title[-1].grid(row=2,column=1,rowspan=2,sticky=NW)
				# Create the final divider line
			self.divider.append(Frame(self.CalendarEntries[-1], bg="White", height = 3, width = 200))
			self.divider[-1].grid(row=4, columnspan=2)


	### End of startup code

	def loophandler40(self):

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
	

