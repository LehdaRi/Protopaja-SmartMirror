import Cfg
import copy
import App_Time
import App_Calendar
import User_Control
import App_Ruokalista
import App_Weather
import App_gmail
import App_Twitter
# This function finds the next possible place to put the application and then puts it there
# It searches down from the given Y coordinate

def Place_App_Corner(app,corner):
	Cfg.root.update()

	OFFSET = 32

	Create_App(app, Cfg.root.winfo_screenwidth()*2, Cfg.root.winfo_screenheight()*2)
	Xtry=OFFSET
	Ytry=OFFSET
	DIRECTION = 1

	if corner[0] == "S":
		Ytry = Cfg.root.winfo_screenheight()-OFFSET-Cfg.app_list[-1].hardheight
		DIRECTION = -1

	if corner[1] == "E":
		Xtry = Cfg.root.winfo_screenwidth()-OFFSET-Cfg.app_list[-1].hardwidth
	

	Ytry = Search_FreePosition(Cfg.app_list[-1],Xtry,Ytry,DIRECTION)
	print("   -- Placing app at: ",Xtry,Ytry)

	if Ytry == 9000:
		print("%ERROR 9000")
		App_Close(Cfg.app_list[-1])
	else:
		Cfg.app_list[-1].Target_X = Xtry
		Cfg.app_list[-1].Target_Y = Ytry
		if corner[1] == "W":
			print("Placing West")
			Cfg.root.update()
			Cfg.app_list[-1].place( x=Xtry-(OFFSET*2)-Cfg.app_list[-1].hardwidth, y=Ytry )
		else:
			print("Placing East")
			Cfg.root.update()
			Cfg.app_list[-1].place( x=Xtry+(OFFSET*2), y=Ytry )

def App_Close(app):
	target = Cfg.app_list.index(app)
	app.destroy()
	Cfg.app_list[target] = None
	App_List_Reorganize()

def App_List_Reorganize():
	for j in range(len(Cfg.app_list)):
		for i in Cfg.app_list:
			if i == None:
				Cfg.app_list.remove(None)




def Check_Collision(TargetX,TargetY,app1,app2):
# Check if objects on the same side of the screen
	if app1 ==  app2:
		return False
	if (app2.winfo_x() < Cfg.root.winfo_screenwidth()/2 and \
		TargetX < Cfg.root.winfo_screenwidth()/2) or \
		(app2.winfo_x() > Cfg.root.winfo_screenwidth()/2 and \
		TargetX > Cfg.root.winfo_screenwidth()/2):
			# Check if either of the objects have conflicting Y edges
		if app2.winfo_y() <= TargetY <= (app2.winfo_y() + app2.hardheight) or \
			app2.winfo_y() <= (TargetY + app1.hardheight) <= (app2.winfo_y() + app2.hardheight) or \
			TargetY <= app2.winfo_y() <= (TargetY + app1.hardheight) or \
			TargetY <= (app2.winfo_y() + app2.hardheight) <= (TargetY + app1.hardheight):
			return True
		else:
			return False
	else:
		return False

def Search_FreePosition(app,TargetX,TargetY,direction):
	OFFSET = 32
	
	for j in range(len(Cfg.app_list)):
		collision = False
		for i in Cfg.app_list:
			collision = Check_Collision(TargetX, TargetY,app,i)
			if collision:
				break
		if collision:	
			if direction == 1:
				TargetY = i.winfo_y()+i.hardheight+OFFSET
				print(" & COLLISION & New TargetY: ",TargetY)
			else:
				TargetY = i.winfo_y()-app.hardheight-OFFSET
				print(" & COLLISION & New TargetY: ",TargetY)
		else:
			if TargetY + app.hardheight > Cfg.root.winfo_screenheight()-31 or \
				TargetY < 31:
				return 9000		
			else:
				print(" & NO COLLISIONS & ")
				return TargetY

def Find_Highest(applist):
	if len(applist) == 1:
		return	applist[0]
	
	stuffs = []

	for i in applist:
		stuffs.append(i.Target_Y)

	return max(stuffs)

def Find_Lowest(applist):
	if len(applist) == 1:
		print(" 1 item lol")
		return	applist[0]
	
	stuffs = []

	for i in applist:
		stuffs.append(i.Target_Y)

	for i in applist:
		if i.Target_Y == min(stuffs):
			return i

def Clear_Apps():
	for i in Cfg.app_list:
		i.exfiltrate()
	"""if Cfg.app_list:
		target = Find_Lowest(Cfg.app_list)
		target.exfiltrate()

		Cfg.root.after(300, Clear_Apps)"""

def Open_User_Apps():
	list = User_Control.UserGetSettings(Cfg.active_user)
	for i in list:

		Create_App(i[0], i[1], i[2])


# This function is used to create applications at given coordintes
# Add to this a new elif line for every new application created
# The name string in the elif statement must be the same as in the apps list
def Create_App(appname, X, Y):

	if appname == "Clock":
		Cfg.app_list.append(App_Time.AppC_Time(Cfg.root,X,Y))
	elif appname == "Calendar":
		Cfg.app_list.append(App_Calendar.AppC_Calendar(Cfg.root,X,Y))
	elif appname == "Ruokalista":
		Cfg.app_list.append(App_Ruokalista.AppC_Ruokalista(Cfg.root,X,Y))
	elif appname == "Weather":
		Cfg.app_list.append(App_Weather.AppC_Weather(Cfg.root,X,Y))
	elif appname == "Gmail":
		Cfg.app_list.append(App_gmail.AppC_Gmail(Cfg.root,X,Y))
	elif appname == "Twitter":
		Cfg.app_list.append(App_Twitter.AppC_Twitter(Cfg.root,X,Y))
	

def Reload_Apps():
	Clear_Apps()
	Open_User_Apps()