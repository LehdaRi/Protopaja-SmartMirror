import urllib.request
import urllib.parse
import random
import string
import time
import hmac
from hashlib import sha1
import base64
import webbrowser
import os
import httplib2
import re

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client.file import Storage

def main():
	print("This program will obtain the user credentials for google and twitter. If incorrect codes are inputed, the user credential files will contain the value 'None'.\n")
	destroyUsers()
	
	while True:
		user_numb = input("User number: ")
		try:
			user_numb = int(user_numb)
			break
		except:
			pass
	
	for i in range(user_numb):
		user = input("Name:")
		goog_cred(user)
		Tw_init(user)
		
def goog_cred(name):
	flow = client.flow_from_clientsecrets(
		'client_secret.json',
		scope='https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.readonly',
		redirect_uri='urn:ietf:wg:oauth:2.0:oob')

	auth_uri = flow.step1_get_authorize_url()
	
	webbrowser.open(auth_uri)

	auth_code = input('Login and enter code here: ')
	file = str(name) + '_goog.txt'
	
	try:
		credentials = flow.step2_exchange(auth_code)
		storage = Storage(file)
		storage.put(credentials)
		return 1
		
	except oauth2client.client.FlowExchangeError:
		fob = open(file, 'w')
		fob.write("None")
		fob.close()
		return 0
		
def Tw_init(name):
	oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
	oauth_timestamp = str(int(time.time()))
	
	values = {'oauth_callback' : 'oob',
				'oauth_consumer_key' : consumerInfo(),
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : 'HMAC-SHA1',
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : '1.0'}
	
	vdict = {}
	for key in values:
		vdict[urllib.parse.quote(key, safe='')] = urllib.parse.quote(values[key], safe='')		
	parameter_str = []
	for key in sorted(vdict):
		parameter_str.append(key)	
		parameter_str.append('=')
		parameter_str.append(vdict[key])
		parameter_str.append('&')
	parameter_str.pop(-1)
	parameter_str = ''.join(parameter_str)
	
	string1 = []
	string1.append('POST')
	string1.append('&')
	string1.append(urllib.parse.quote('https://api.twitter.com/oauth/request_token', safe=''))
	string1.append('&')
	string1.append(urllib.parse.quote(parameter_str, safe=''))
	string1 = ''.join(string1)
	
	signing_key = urllib.parse.quote(consumerInfo('secret'), safe='') + '&'
	hashed = hmac.new(signing_key.encode('utf-8'), string1.encode('utf-8'), sha1)
	values['oauth_signature'] = urllib.parse.quote(base64.b64encode(hashed.digest()), safe='')
	
	DST = []
	DST.append('OAuth ')					
	for key in sorted(values):									
		DST.append(urllib.parse.quote(key, safe=''))
		DST.append('="')
		if key == 'oauth_signature':
			DST.append(values[key])
		else:
			DST.append(urllib.parse.quote(values[key], safe=''))
		DST.append('"')
		DST.append(', ')
	DST.pop(-1)
	DST = ''.join(DST)

	HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/oauth/request_token')
	HTTP_REQUEST.add_header("Authorization", DST)
	resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())
	
	oauth_token = ''.join(re.findall(r"n=(.*?)&", resp))
	oauth_token_secret = ''.join(re.findall(r"t=(.*?)&", resp))
	
	resp_url = 'https://api.twitter.com/oauth/authenticate' + '?' + ''.join(re.findall(r"b'(.*?)&", resp))
	webbrowser.open(resp_url)
	
	PIN = input("Login and enter code here: ")
	
	oauth_nonce = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(42))
	oauth_timestamp = str(int(time.time()))
	
	values = {'oauth_token' : oauth_token,
				'oauth_consumer_key' : consumerInfo(),
				'oauth_nonce' : oauth_nonce,
				'oauth_signature_method' : 'HMAC-SHA1',
				'oauth_timestamp' : oauth_timestamp,
				'oauth_version' : '1.0',
				'oauth_verifier' : PIN}

	vdict = {}
	for key in values:
		vdict[urllib.parse.quote(key, safe='')] = urllib.parse.quote(values[key], safe='')		
	parameter_str = []
	for key in sorted(vdict):
		parameter_str.append(key)	
		parameter_str.append('=')
		parameter_str.append(vdict[key])
		parameter_str.append('&')
	parameter_str.pop(-1)
	parameter_str = ''.join(parameter_str)
	
	string1 = []
	string1.append('POST')
	string1.append('&')
	string1.append(urllib.parse.quote('https://api.twitter.com/oauth/access_token', safe=''))
	string1.append('&')
	string1.append(urllib.parse.quote(parameter_str, safe=''))
	string1 = ''.join(string1)
	
	signing_key = urllib.parse.quote(consumerInfo('secret'), safe='') + '&' + urllib.parse.quote(oauth_token_secret, safe='')
	hashed = hmac.new(signing_key.encode('utf-8'), string1.encode('utf-8'), sha1)
	values['oauth_signature'] = urllib.parse.quote(base64.b64encode(hashed.digest()), safe='')

	DST = []
	DST.append('OAuth ')					
	for key in sorted(values):									
		DST.append(urllib.parse.quote(key, safe=''))
		DST.append('="')
		if key == 'oauth_signature':
			DST.append(values[key])
		else:
			DST.append(urllib.parse.quote(values[key], safe=''))
		DST.append('"')
		DST.append(', ')
	DST.pop(-1)
	DST = ''.join(DST)
	
	file = str(name) + '_tw.txt'
	
	try:
		HTTP_REQUEST = urllib.request.Request('https://api.twitter.com/oauth/access_token')
		HTTP_REQUEST.add_header("Authorization", DST)
		resp = str(urllib.request.urlopen(HTTP_REQUEST, bytes('', 'ascii')).read())
		
		o_token = ''.join(re.findall(r"n=(.*?)&", resp))
		s_token = ''.join(re.findall(r"t=(.*?)&", resp))
	
		fob = open(file, 'w')
		lines = [o_token + '\n', s_token]
		fob.writelines(lines)
		fob.close()
		return 1
		
	except urllib.error.HTTPError:
		fob = open(file, 'w')
		lines = ["None\n", "None"]
		fob.writelines(lines)
		fob.close()
		return 0
		
def consumerInfo(type='key'):
	fob = open('Tw_secret.txt', 'r')
	lines = fob.readlines()
	fob.close()
	if type is 'secret':
		consumer_secret = ''.join(re.findall(r'consumer_secret: (.*?)\n', lines[1]))
		return consumer_secret
	else:
		consumer_key = ''.join(re.findall(r'consumer_key: (.*?)\n', lines[0]))
		return consumer_key
	
def destroyUsers():
	files = os.listdir(os.getcwd())
	cred_files = []
	for file in files:
		a = ''.join(re.findall(r'\S*_goog.txt', file))
		b = ''.join(re.findall(r'\S*_tw.txt', file))
		if a:
			cred_files.append(a)
		if b:
			cred_files.append(b)		
	
	for file in cred_files:
		os.remove(file)

if __name__ == '__main__':
	main()