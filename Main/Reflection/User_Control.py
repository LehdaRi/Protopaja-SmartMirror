import Cfg
import wifsm2
import api_init3
import copy
import AppControl

def UserCreate(user):
	api_init3.goog_cred(user)
	api_init3.Tw_init(user)

def UserLogIn(user):
	j=wifsm2.getUsers()
	Cfg.active_user = j[user][0]
	AppControl.Reload_Apps()



def UserGetSettings(user):
	try:
		file = open('UserSettings.txt', 'r')
	except:
		file = open('UserSettings.txt', 'w')
		default="Default;"
		default+="Clock 1720 32;"
		default+="Weather 1682 202;"
		default+="Ruokalista 32 32"
		file.write(default)
		file.close()
		file = open('UserSettings.txt', 'r')
	lines = file.read().splitlines()
	for i in lines:
		info = []
		data = i.split(";")

		if data[0] == user:
			del data[0]
			for j in data:
				info.append(j.split())
			return info

	

def UserSaveSettings():
	try:
		file = open('UserSettings.txt', 'a')
	except:
		file = open('UserSettings.txt', 'w')
		default="Default;"
		default+="Clock 1720 32;"
		default+="Weather 1682 202;"
		default+="Ruokalista 32 32"
		file.write(default)
		file = open('UserSettings.txt', 'a')
		file.close()
	string = copy.copy(Cfg.active_user)
	for i in Cfg.app_list:
		string += ";" + i.name + " " + str(i.Target_X) + " " + str(i.Target_Y)
	file.write("\n" + str(string))
	

