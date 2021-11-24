import urllib.request
from bs4 import BeautifulSoup
import json
import parser

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'}

#Returns a CSRF token
def getToken():
	req = urllib.request.Request('https://psmobile.pitt.edu/app/catalog/classSearch')
	response = urllib.request.urlopen(req)
	return response.info()['Set-Cookie'][11:43]
	
#Returns a BeautifulSoup Object for the given academic career and subject
#BeautifulSoup Object contains all HTML from response
def getSubjectSoup(token, acad_career, subject):
	data = bytes("CSRFToken=" + token + "&term=2221&campus=PIT&acad_career=" + acad_career + "&crse_attr=&crse_attr_value=&subject=" + subject + "&catalog_nbr=&class_nbr=", encoding="utf-8")
	req = urllib.request.Request('https://psmobile.pitt.edu/app/catalog/getClassSearch', data, headers)
	with urllib.request.urlopen(req) as response:
		soup = BeautifulSoup(response.read(), 'html.parser')
	return soup

#Returns a list of lists returned by getClassInfo for each class at Pitt
def getClasses():
	token = getToken()
	classes = []
	headers["Cookie"] = "CSRFCookie="+token
	with open("subjects.json") as jsubs:
		subjects = json.load(jsubs)
	for subject in subjects:
		print("Getting all classes in " + subject['subject'])
		for campus in subject['campuses'].values():
			if (campus['campus'] == 'PIT'):
				for career in subject['careers'].values():
					soup = getSubjectSoup(token, career['career'], subject['subject'])
					cls = getClassInfo(soup)
					classes.append(cls)
	return classes

#Returns a list of lists with info about all classes found in subject soup
def getClassInfo(soup):
	ret = []
	classes = soup.find_all('div',{'class':'section-content'})
	for cls in classes:
		div = cls.find('div',{'class':'section-body'}).next_sibling.next_sibling.next_sibling.next_sibling
		days = parser.parseDays(div.string[12:])
		div = div.next_sibling.next_sibling
		rooms = parser.parseRooms(div.string[6:])
		div = div.next_sibling.next_sibling.next_sibling.next_sibling
		dates = parser.parseDates(div.string[15:])
		ret.append([days, dates, rooms])
	return ret

def testClasses():
	token = getToken()
	classes = []
	headers["Cookie"] = "CSRFCookie="+token
	soup = getSubjectSoup(token, 'UGRD', 'PHYS')
	cls = getClassInfo(soup)
	classes.append(cls)
	return classes