from tkinter import*
import urllib.request
from PIL import Image
import os

import Cfg
from time import*

import wifsm2

class AppC_Twitter(Frame):
	def __init__(self, parent,X,Y):

	#### Initiate object variables
	# Variables for system operation
		self.Target_X = X
		self.Target_Y = Y
		self.Xmove=0
		self.Ymove=0
		self.speedy=2
		self.speedx=2
		self.name = "Twitter"
		self.hardheight = 936
		self.hardwidth = 658
		

	# Class specific variables for object operation
		

	### End of variables

	### Execute startup code

			# Create frame for the app and place at given coordinates
		Frame.__init__(self, parent)
		Frame.config(self, bg="#000000")
		self.place(x=X, y=Y)

	
	### Draw the app
	
		files = os.listdir(os.getcwd())
		for file in files:
			a = ''.join(re.findall(r'profile_pic\S*.png', file))
			print(a)
			if a:
				os.remove(file)
	
		response = wifsm2.getHomeTimeline(Cfg.active_user, tweet_numb=10)
		
		image1 = PhotoImage(file = 'images\\2110817.png')
		
		Label(self, text = 'Twitter' , fg="white", bg="Black", font=("Helvetica", 16)).grid(row=0, column=1, columnspan=2, sticky=W)
		icon = Label(self, image=image1, borderwidth=0, highlightthickness=0)
		icon.image = image1
		icon.grid(row=0, column=0)
		
		numb = 1
		for tweet in response:
			
			picture = 'profile_pic' + str(numb)
			urllib.request.urlretrieve(tweet["picture"], picture  + '.jpg')
			img = Image.open(picture  + '.jpg')
			img.save(picture + '.png')
			os.remove(picture + '.jpg')
			image = PhotoImage(file = picture + '.png')
			icon = Label(self, image=image)
			icon.image = image
			icon.grid(row=numb, rowspan = 2, column=1, columnspan = 2, padx = 10, pady = 10)
			
			s1 = ''
			s2 = ''
			s3 = ''
			ccount = 1
			for c in tweet["text"]:
				if ccount <= 90:
					s1 = s1 + c
				elif ccount <= 180 and ccount > 90:
					if ccount == 91 and c == ' ':
						pass
					else:
						s2 = s2 + c
				elif ccount <= 270 and ccount > 180:
					if ccount == 181 and c == ' ':
						pass
					else:
						s3 = s3 + c
				ccount = ccount + 1
			
			Label(self, text=tweet["name"] , fg="white", bg="Black", font=("Helvetica", 12)).grid(row=numb, column=3, sticky=W)
			Label(self, text=tweet["id"] , fg="white", bg="Black", font=("Helvetica", 10)).grid(row=numb, column=4, sticky=W)
			Label(self, text=tweet["time"] , fg="white", bg="Black", font=("Helvetica", 7)).grid(row=numb, column=5, sticky=W)
			numb = numb + 1
			Label(self, text=s1 , fg="white", bg="Black", font=("Helvetica", 10)).grid(row=numb, column=3, columnspan = 3, sticky=W)
			if s2 != '':
				numb = numb + 1
				Label(self, text=s2 , fg="white", bg="Black", font=("Helvetica", 10)).grid(row=numb, column=3, columnspan = 3, sticky=W)
			if s3 != '':
				numb = numb + 1
				Label(self, text=s3 , fg="white", bg="Black", font=("Helvetica", 10)).grid(row=numb, column=3, columnspan = 3, sticky=W)
			numb = numb + 1

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


	def loophandler1000(self):
		#print(self.winfo_width(),self.winfo_height())
		pass

	def loophandler60000(self):
		pass
	
	'''numb = 0
		for file in files:
			if file.endswith('.txt'):
				a = ''.join(re.findall(r'\d', file))
				print(a)
				numb = int(numb)
				if numb < int(a):
					numb = a
					print(numb)
		
		numb = numb + 1
		
		pic_names = []

		for tweet in response:
			check = 0
			for file in files:
				if file.endswith('.txt'):
					fob = open(file, 'r')
					url = fob.read()
					if url == tweet["picture"]:
						pic_names.append(''.join(re.findall(r'(.*?).txt', fob.name)) + '.png')
						check = 1
						break		
					
					fob = open(picture_url, 'w')
			fob.write(tweet["picture"])
			fob.close()
					
					'''
					

