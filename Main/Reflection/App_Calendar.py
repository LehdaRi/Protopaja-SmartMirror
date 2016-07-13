from tkinter import*

from Config import*

import wifsm

class AppC_Calendar(Frame):
	def __init__(self, parent,X,Y):
		global active_user
		active_user = wifsm.User(0)
	#### Initiate object variables
	# Variables for system operation
		self.X = X
		self.Y = Y
		self.name = "Calendar"

	# Class specific variables for object operation

			# Get calendar entries
		self.events = active_user.getCalendarEvents()
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
		self.place(x=self.X, y=self.Y)
		
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
		pass

	def loophandler1000(self):
		pass

	def loophandler60000(self):
		pass
	

