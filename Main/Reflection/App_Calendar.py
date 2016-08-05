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
		self.hardheight = 337
		self.hardwidth = 200

	# Class specific variables for object operation

			# Get calendar entries
		self.events = wifsm2.calendarList(Cfg.active_user,event_numb=5)
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
			print(i)
		if len(self.events) == 0:
			self.none = Label(self, text = "Calendar empty", fg="white", bg="Black", font=("Helvetica", 16))
			self.none.pack()

		for j in range(len(self.events)):
			i = self.events[j]
			junk = i["start"]
			if j > 0:
				junk2 = self.events[j]["start"]
			else:
				junk2 = [0,0,0]
			
		# Create frame to hold the calendar entry
			self.CalendarEntries.append(Frame(self, bg="Black"))
			self.CalendarEntries[-1].pack()
				# Create label with the date
			if (j == 0) or not (junk[2]==junk2[2] and junk[1]==junk2[1] and junk[0] == junk2[0]):
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
	def exfiltrate(self):
		if self.winfo_x() < Cfg.root.winfo_screenwidth()/2:
			self.Target_X = self.winfo_x()-32- 32-self.hardwidth
		else:
			self.Target_X = self.winfo_x() + 32 + 32 + self.hardwidth
		self.doomed = True
	def loophandler40(self):

		### Move animation
		self.Target_Y = int(self.Target_Y)
		self.Target_X = int(self.Target_X)
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
			if self.doomed ==  True:
				self.destroy()

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
	

