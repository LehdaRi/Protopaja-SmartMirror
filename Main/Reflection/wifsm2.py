import urllib.request
import urllib.parse
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
		result = {'id': id, 'name': name, 'time': time, 'text': text, 'picture': str(tweet.user.profile_image_url)}
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
		junk = event["start"]["dateTime"]
		stuff["start"] = [junk[:4], junk[5:7], junk[8:10],junk[11:13],junk[14:16],junk[17:19]]
		junk = event["end"]["dateTime"]
		stuff["end"] = [junk[:4], junk[5:7], junk[8:10],junk[11:13],junk[14:16],junk[17:19]]
		stuff["title"] = event['summary']
		elist.append(stuff)
	
	print(elist)	
	return elist
	
def getRuokalistatT():

	url = 'http://www.lounasaika.net/api/v1/menus.json'
	
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	str1 = '' 
	for line in response:
		a = line.decode('utf8')
		str1 = str1 + a
	
	restaurants = re.findall(r'({"name":.*?"meals":.*?})', str1)
	
	foodlist = []
	for restaurant in restaurants:
		campus = ''.join(re.findall(r'"campus":"(.*?)"', restaurant))
		ota = re.findall(r'[oO][tT][aA]', campus)
		if ota:
			dict1 = {}
			dict1["name"] = ''.join(re.findall(r'"name":"(.*?)"', restaurant))
			meals = ''.join(re.findall(r'"meals":{"fi":(.*?),"en"', restaurant))
			#print(name + ' : ' + campus)
			print('\n\n')
			print(meals)
			#print(restaurant)
			
	
def getRuokalistat():
	
	response = urllib.request.urlopen('http://ruokalistat.net/')
	
	response = str(response.read())
	
	foods = {}
	
	food1 = ''.join(re.findall(r'<!-- ruuat1 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Tietotekniikkatalo"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat2 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Täffä"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat3 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro').replace('\\xc3\\x80', 'A')
		food4.append(a)
	foods["Alvari"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat4 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["--"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat5 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Sähkötekniikka"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat6 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Kvarkki"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat7 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Tuas"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat8 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Elektra"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat9 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Kasper"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat10 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Konetekniikka"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat11 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Aalto Valimo"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat12 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Tietotie 6"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat13 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["VM5"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat14 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Antell-ravintola Calori"] = food4
	
	food1 = ''.join(re.findall(r'<!-- ruuat15 -->\\n(.*?)</td>', response))
	food2 = re.findall(r'\\t(.*?)<br />', food1)
	food3 = re.findall(r'\\n(.*?)<br />', food1)
	for f in food3:
		food2.append(f)
	food4 = []
	for f in food2:
		a = f.replace('\\xc3\\xa4', 'ä').replace('\\xc3\\xb6', 'ö').replace('\\xe2\\x82\\xac', 'euro')
		food4.append(a)
	foods["Mau-kas"] = food4
	
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
	
def getWeather(woeid=570736):
	
	url = "https://query.yahooapis.com/v1/public/yql"
	
	yql_query = "select * from weather.forecast where woeid=" + str(woeid) + " and u='c'"
	
	values = {'q': yql_query, 'format': 'json'}
	
	data = urllib.parse.urlencode(values)
	data = data.encode('utf-8')
	
	req = urllib.request.Request(url, data)
	response = str(urllib.request.urlopen(req).read())
	
	forecast = ''.join(re.findall(r'"forecast":\[(.*?)\],', response))
	
	forecastlist = re.findall(r'{(.*?)}', forecast)
	weatherweek = []
	for day in forecastlist:
		
		dict1 ={}
		dict1["date"] = ''.join(re.findall(r'"date":"(.*?)"', day))
		dict1["day"] = ''.join(re.findall(r'"day":"(.*?)"', day))
		dict1["high"] = ''.join(re.findall(r'"high":"(.*?)"', day))
		dict1["low"] = ''.join(re.findall(r'"low":"(.*?)"', day))
		dict1["text"] = ''.join(re.findall(r'"text":"(.*?)"', day))
		weatherweek.append(dict1)
	
	return weatherweek
	
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
	pass