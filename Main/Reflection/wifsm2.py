import urllib.request
import httplib2
import string
letters = string.printable + 'äöå'
import os
import re
import datetime

import tweepy

from oauth2client.file import Storage
from oauth2client import client
from apiclient import discovery
from apiclient.http import BatchHttpRequest
	
def getHomeTimeline(user, tweet_numb=10):

	file = str(user) + '_tw.txt'
	
	def Tw_consumerInfo(type='key'):
		fob = open('Tw_secret.txt', 'r')
		lines = fob.readlines()
		fob.close()
		if type is 'secret':
			consumer_secret = ''.join(re.findall(r'consumer_secret: (.*?)\n', lines[1]))
			return consumer_secret
		else:
			consumer_key = ''.join(re.findall(r'consumer_key: (.*?)\n', lines[0]))
			return consumer_key
		
	def Tw_getKey(type=None):
		fob = open(file, 'r')
		lines = fob.readlines()
		fob.close()
		if type is 'secret':
			return lines[1]
		else:
			token = ''.join(re.findall(r'(.*?)\n', lines[0]))
			return token
	
	auth = tweepy.OAuthHandler(Tw_consumerInfo(), Tw_consumerInfo("secret"))
	api = tweepy.API(auth)
	auth.set_access_token(Tw_getKey(), Tw_getKey('secret'))
	
	public_tweets = api.home_timeline(count=tweet_numb)
	
	tweets = []
	for tweet in public_tweets:
		string1 = ''
		for c in tweet.text:
			if c in letters:
				string1 = string1 + c
			else:
				string1 = string1 + '(?)'
		text = string1
		id = '@' + tweet.user.screen_name
		name = str(tweet.user.name)
		time = str(tweet.created_at)
		result = {'id': id, 'name': name, 'time': time, 'text': text}
		tweets.append(result)
		
	return tweets
	
def emailList(user, email_numb=5):
	
	response_list = []
	
	def batchResponse(request_id, response, exception):
	
		if exception is not None:
			response_list.append(exception)
			return 0
		else:
			response_list.append(response)
			return 1
	
	file = str(user) + '_goog.txt'
	storage = Storage(file)

	credentials = storage.get()
	http_auth = credentials.authorize(httplib2.Http())
	
	service2 = discovery.build('gmail', 'v1', http_auth)
	
	results = service2.users().messages().list(userId='me', q='[ in:inbox -category:{social promotions forums} ]', maxResults = email_numb).execute()['messages']
	
	batch_request = service2.new_batch_http_request()
	
	for result in results:
		batch_request.add(service2.users().messages().get(userId='me', id=str(result['id']), format='metadata'), callback=batchResponse)
	batch_request.execute()
	
	message_list = []
	for response in response_list:
		headers = response['payload']['headers']
		subject = ''
		fromuser = ''
		datesent = ''
		for item in headers:
			if item["name"] == 'Subject':
				subject = item["value"]
			if item["name"] == 'From':
				fromuser = item["value"]
			if item["name"] == 'Date':
				datesent = item["value"]
		string1 = ''
		string2 = ''
		for c in subject:
			if c in letters:
				string1 = string1 + c
			else:
				string1 = string1 + '(?)'
		for c in fromuser:
			if c in letters:
				string2 = string2 + c
			else:
				string2 = string2 + '(?)'
		message_list.append({'Subject': string1, 'From': string2, 'Date': datesent})
	
	return message_list
	
def calendarList(user, event_numb=5):

	file = str(user) + '_goog.txt'
	storage = Storage(file)

	credentials = storage.get()
	http_auth = credentials.authorize(httplib2.Http())
	
	now = datetime.datetime.utcnow().isoformat() + 'Z'
	
	service1 = discovery.build('calendar', 'v3', http_auth)
	events = service1.events().list(calendarId='primary', timeMin=now, maxResults=event_numb).execute()['items']
	
	elist = []
	for event in events:
		stuff = {}
		stuff["start"] = event["start"]["dateTime"]
		stuff["end"] = event["end"]["dateTime"]
		stuff["title"] = event['summary']
		elist.append(stuff)
		
	return elist
	
def getRuokalistat():
	
	response = urllib.request.urlopen('http://ruokalistat.net/')
	response = str(response.read())
	
	foods = []
	
	food1 = ''.join(re.findall(r'<!-- ruuat1 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Tietotekniikkatalo": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat2 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Täffä": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat3 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Alvari": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat4 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"--": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat5 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Sähkötekniikka": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat6 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Kvarkki": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat7 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"TUAS": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat8 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Electra": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat9 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Kasper": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat10 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Konetekniikka": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat11 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Aalto Valimo": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat12 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Tietotie 6": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat13 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"VM5": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat14 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Antell-ravintola Calori": food2}
	foods.append(dict1)
	
	food1 = ''.join(re.findall(r'<!-- ruuat15 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	dict1 = {"Mau-kas": food2}
	foods.append(dict1)
	
	return foods
	
def getNow(utc_add=3):
	
	now = str(datetime.datetime.utcnow())
	now = now.split()[1].split(':')
	now[0] = str(int(now[0]) + utc_add)
	now = ':'.join(now)
	
	time = str(datetime.datetime.utcnow())
	time = time.split('T')[0].split()
	time[1] = now
	time = 'T'.join(time)
	
	return time
	
def getUsers():
	
	files = os.listdir(os.getcwd())
	cred_files = []
	for file in files:
		a = ''.join(re.findall(r'\S*_goog.txt', file))
		if a:
			cred_files.append(a)
	
	users = []
	for file in cred_files:
		storage = Storage(file)
		
		credentials = storage.get()
		http_auth = credentials.authorize(httplib2.Http())
		
		service3 = discovery.build('gmail', 'v1', http_auth)
		
		result = service3.users().getProfile(userId='me').execute()['emailAddress']
		name = ''.join(re.findall(r'(.*?)_goog.txt', file))
		list1 = [name, result]
		users.append(list1)
	
	return users

if __name__ == '__main__':
	print("Four main functions: getHomeTimeline, emailList, calendarList, and getRuokalistat.")