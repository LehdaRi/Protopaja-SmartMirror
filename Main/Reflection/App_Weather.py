from tkinter import*

import wifsm2
import Cfg
from time import*


class AppC_Weather(Frame):
	def __init__(self, parent,X,Y):

	#### Initiate object variables
	# Variables for system operation
		self.Target_X = X
		self.Target_Y = Y
		self.Xmove=0
		self.Ymove=0
		self.speedy=2
		self.speedx=2
		self.name = "Weather"
		self.hardheight = 468
		self.hardwidth = 206
		self.doomed = False
	# Class specific variables for object operation
		self.weather = wifsm2.getWeather()

		self.pics = []
		self.Thunderstorms = PhotoImage(file = "images/Weather/Thunderstorms.gif")
		



	### End of variables

	### Execute startup code

			# Create frame for the app and place at given coordinates
		Frame.__init__(self, parent)
		Frame.config(self, bg="#FFF000")
		self.place(x=X, y=Y)


	
	### Draw the app
		self.weatherframes = [Frame(self, bg="Black"),Frame(self, bg="Black"),Frame(self, bg="Black")]
		for i in self.weatherframes:
			i.pack()
		self.weatherelements = [[],[],[]]

		for i in range(3):
			self.weatherelements[i].append(Label(self.weatherframes[i], text = self.weather[i]["day"],\
													fg="white", bg="Black", font=("Helvetica", 24)))
			self.weatherelements[i].append(Label(self.weatherframes[i], text = self.weather[i]["high"] + " C",\
													fg="white", bg="Black", font=("Helvetica", 24)))
			self.weatherelements[i].append(Label(self.weatherframes[i], text = self.weather[i]["low"]+ " C",\
													fg="white", bg="Black", font=("Helvetica", 24)))
			self.weatherelements[i].append(Label(self.weatherframes[i], text = self.weather[i]["text"],\
													fg="white", bg="Black", font=("Helvetica", 12)))

			print(self.weather[i]["text"])
			if self.weather[i]["text"] in ["Tornado","Tropical Storm","Hurricane","Severe Thunderstorms",\
											"Thunderstorms","Isolated Thunderstorms","Scattered Thunderstorms",\
											"Scattered Thunderstorms","Thundershowers","Isolated Thundershowers"]:
				self.pics.append(PhotoImage(file = "images/Weather/Thunderstorms.gif"))
			elif self.weather[i]["text"] in ["Clear (Night)","Sunny","Fair (Night)","Fair (Day)","Hot","Cold"]:
				self.pics.append(PhotoImage(file = "images/Weather/Sunny.gif"))
			elif self.weather[i]["text"] in ["Mixed Rain And Snow","Mixed Rain And Sleet","Mixed Snow And Sleet",\
											"Freezing Dizzle","Snow Flurries","Light Snow Showers","Blowing Snow",\
											"Snow","Hail","Sleet","Mixed Rain And Hail","Heavy Snow",\
											"Scattered Snow Showers","Heavy Snow","Snow Showers"]:
				self.pics.append(PhotoImage(file = "images/Weather/Snow.gif"))
			elif self.weather[i]["text"] in ["Frizzle","Scattered Showers"]:
				self.pics.append(PhotoImage(file = "images/Weather/Slight Drizzle.gif"))
			elif self.weather[i]["text"] in ["Freezing Rain","Showers"]:
				self.pics.append(PhotoImage(file = "images/Weather/Rain.gif"))
			elif self.weather[i]["text"] in ["Cloudy","Mostly Cloudy (Night)","Mostly Cloudy (Day)"]:
				self.pics.append(PhotoImage(file = "images/Weather/Cloudy.gif"))
			elif self.weather[i]["text"] in ["Partly Cloudy (Night)","Partly Cloudy (Day)","Partly Cloudy"]:
				self.pics.append(PhotoImage(file = "images/Weather/Mostly Cloudy.gif"))
			else:
				self.pics.append(PhotoImage(file = "images/Weather/Haze.gif"))
			
			self.weatherelements[i].append(Label(self.weatherframes[i], image = self.pics[i],\
													fg="white", bg="Black", font=("Helvetica", 16)))
			self.weatherelements[i][0].grid(row = 0, column = 1)
			self.weatherelements[i][1].grid(row = 1, column = 1)
			self.weatherelements[i][2].grid(row = 2, column = 1)
			self.weatherelements[i][3].grid(row = 3, column = 0, columnspan = 2)
			self.weatherelements[i][4].grid(row = 0, column = 0, rowspan = 3)




	### End of startup code
	def exfiltrate(self):
		if self.winfo_x() < Cfg.root.winfo_screenwidth()/2:
			self.Target_X = self.winfo_x()-32- 32-self.hardwidth
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
		pass

	def loophandler60000(self):
		pass
	

