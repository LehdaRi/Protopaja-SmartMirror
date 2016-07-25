import Cfg
import wifsm2
import api_init3


def UserCreate(user):
	api_init3.goog_cred(user)
	api_init3.Tw_init(user)

def UserLogIn(user):
	j=wifsm2.getUsers()
	Cfg.active_user = j[user][0]