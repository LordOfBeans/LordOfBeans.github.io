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
		ret.append([days, dates, rooms])
	return ret

def minTime(hour, min):
	return hour * 60 + min

#Please forgive me for this abomination of ifs, elses, and loops
def buildClassDict():
	token = getToken()
	classDict = {}
	headers["Cookie"] = "CSRFCookie="+token
	with open("subjects.json") as jsubs:
		subjects = json.load(jsubs)
	for subject in subjects:
		for campus in subject['campuses'].values():
			if campus['campus'] == 'PIT':
				for career in subject['careers'].values():
					print("Retrieving all classes in " + career['career'] + " " + subject['subject'])
					subjectSoup = getSubjectSoup(token, career['career'], subject['subject'])
					subjectClasses = subjectSoup.find_all('div', {'class':'section-content'})
					for cls in subjectClasses:
						div = cls.find('div',{'class':'section-body'}).next_sibling.next_sibling.next_sibling.next_sibling
						days = parser.parseDays(div.string[12:])
						div = div.next_sibling.next_sibling
						rooms = parser.parseRooms(div.string[6:])
						for i in range(0, len(rooms)):
							day = days[i]
							room = rooms[i]
							if room != None and day != None:
								for j in range(0, len(day[0])):
									weekday = day[0][j]
									times = day[1:]
									building = room[0]
									roomNum = room[1]
									if weekday in classDict.keys():
										if building in classDict[weekday].keys():
											if roomNum in classDict[weekday][building].keys():
												index = 0
												roomList = classDict[weekday][building][roomNum]
												while index < len(roomList) and minTime(roomList[index][2], roomList[index][3]) < minTime(times[0], times[1]):
													index += 1
												if index < len(roomList):
													#If there is no overlap
													if minTime(roomList[index][0], roomList[index][1]) > minTime(times[2], times[3]):
														roomList.insert(index, times)
													else:
														if times != roomList[index]:
															print("Imperfect time overlap detected in " + room[0] + " " + room[1] + " on " + weekday)
															print("\tNew class time: " + parser.timesToString(times))
															print("\tPlaced class time: " + parser.timesToString(roomList[index]))
															new_index = index
															while new_index < len(roomList) and minTime(roomList[new_index][0], roomList[new_index][1]) <= minTime(times[2], times[3]):
																new_index+=1
															if minTime(roomList[index][0], roomList[index][1]) <= minTime(times[0], times[1]):
																startTime = [roomList[index][0], roomList[index][1]]
															else:
																startTime = [times[0], times[1]]
															if minTime(roomList[new_index - 1][2], roomList[new_index - 1][3]) >= minTime(times[2], times[3]):
																	endTime = [roomList[new_index - 1][2], roomList[new_index - 1][3]]
															else:
																endTime = [times[2], times[3]]
															print("\tReplacing: ")
															for i in range(index, new_index):
																print("\t\t" + parser.timesToString(roomList[i]))
															print ("\t\twith " + parser.timesToString(startTime+endTime))
															parser.timeReplace(roomList, index, new_index, startTime + endTime)
												else:
													roomList.append(times)
											else:
												classDict[weekday][building][roomNum] = [times]
										else:
											classDict[weekday][building] = {roomNum:[times]}
									else:
										classDict[weekday] = {building:{roomNum:[times]}}
	return classDict

	

def testClasses():
	token = getToken()
	classes = []
	headers["Cookie"] = "CSRFCookie="+token
	soup = getSubjectSoup(token, 'UGRD', 'PHYS')
	cls = getClassInfo(soup)
	classes.append(cls)
	return classes
