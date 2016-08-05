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
		self.hardheight = 530
		self.hardwidth = 744
		

	# Class specific variables for object operation
		

	### End of variables

	### Execute startup code

			# Create frame for the app and place at given coordinates
		Frame.__init__(self, parent)
		Frame.config(self, bg="#000000")
		self.place(x=X, y=Y)

	
	### Draw the app
		
		response = wifsm2.emailList(Cfg.active_user, 10)
	
		image = PhotoImage(file = 'images\\2110816.png')
		
		Label(self, text = 'Gmail' , fg="white", bg="Black", font=("Helvetica", 16)).grid(row=0, column=1, columnspan=2, sticky=W)
		icon = Label(self, image=image, borderwidth=0, highlightthickness=0)
		icon.image = image
		icon.grid(row=0, column=0)
		
		row = 1
		for email in response:
			name = ''.join(re.findall(r'<(.*?)>', email['From']))
			s1 = ''
			s2 = ''
			s3 = ''
			ccount = 1
			for c in email["Subject"]:
				if ccount <= 60:
					s1 = s1 + c
				elif ccount <= 120 and ccount > 60:
					if ccount == 61 and c == ' ':
						pass
					else:
						s2 = s2 + c
				elif ccount <= 180 and ccount > 120:
					if ccount == 121 and c == ' ':
						pass
					else:
						s3 = s3 + c
				ccount = ccount + 1
			Label(self, text=name , fg="white", bg="Black", font=("Helvetica", 12)).grid(row=row, column=1, sticky=W)
			Label(self, text=s1, fg="white", bg="Black", font=("Helvetica", 10)).grid(row=row, column=2, sticky=W)
			row = row + 1
			Label(self, text=s2, fg="white", bg="Black", font=("Helvetica", 10)).grid(row=row, column=2, sticky=W)
			Label(self, text=email['Date'], fg="white", bg="Black", font=("Helvetica", 7)).grid(row=row, column=1, sticky=W)
			if s3 != '':
				row = row + 1	
				Label(self, text=s3, fg="white", bg="Black", font=("Helvetica", 10)).grid(row=row, column=2, sticky=W)
			row = row + 1		

	### End of startup code

	def loophandler40(self):
		


		### Move animation handling below ###
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
		### Move animation above this line ###


	def loophandler1000(self):
		#print(self.winfo_width(),self.winfo_height())
		pass

	def loophandler60000(self):
		pass
	

