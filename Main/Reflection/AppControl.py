from Config import*
import copy
import App_Time
import App_Calendar


# This function finds the next possible place to put the application and then puts it there
# It searches down from the given Y coordinate
def Place_App(app,X,Y):
	global app_list
	Xtry = copy.copy(X)
	Ytry = copy.copy(Y)

	if len(app_list) == 0:
		Create_App(app, Xtry, Ytry)
	else:
		for j in range(10):
			j-=1
			for i in app_list:
				if not i.Y <= Ytry <= i.Y + i.winfo_height():
					Create_App(app, Xtry, Ytry)
					break
				else:
					Ytry = i.Y + i.winfo_height() + 32
			else:
				continue
			break

# This function is used to create applications at given coordintes
# Add to this a new elif line for every new application created
# The name string in the elif statement must be the same as in the apps list
def Create_App(appname, X, Y):
	if appname == "Clock":
		app_list.append(App_Time.AppC_Time(root,X,Y))
	elif appname == "Calendar":
		app_list.append(App_Calendar.AppC_Calendar(root,X,Y))