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

def minTime(hour, min):
	return hour * 60 + min

#My apologies for this abomination of code. No method this simple in concept should be this long, but it works so I'm running with it.
#Returns a dictionary with the format {Weekday:{Building:{Room:[Times]}}}
#Times in the innermost list are 4-length list with format [start_hour, start_minute, end_hour, end_minute]
#This is not a complete dictionary of all classes and times at Pitt. It is specifically configured for finding openings in classrooms. Overlapping classes are put together. Classes that contradict posted building hours are trimmed. No information on subject, professor, class number, class size, specific dates, etc. are stored.
#This project in general also has a very specific purpose. The code here would require a lot of adaptation to be used for purposes other than finding openings.
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
									hours = parser.getBuildingHours(room[0], weekday)
									times = day[1:]
									building = room[0]
									roomNum = room[1]
									if hours == None:
										print(parser.timesToString(times) + " class in " + roomNum + " " + building + " despite closure on " + weekday)
										continue
									else:
										building_open = minTime(hours[0], hours[1])
										building_close = minTime(hours[2], hours[3])
										class_start = minTime(times[0], times[1])
										class_end = minTime(times[2], times[3])
									if building_open > class_start:
										print(parser.timesToString(times) + " class in " + roomNum + " " + building + " despite opening at " + parser.timeToString(hours[0], hours[1]) + " on " + weekday)
										times[0] = hours[0]
										times[1] = hours[1]
										print("\tChanged times to " + parser.timesToString(times))
									if building_close < class_end:
										print(parser.timesToString(times) + " class in " + roomNum + " " + building + " despite closing at " + parser.timeToString(hours[2], hours[3]) + " on " + weekday)
										times[2] = hours[2]
										times[3] = hours[3]
										print("\tChanged times to " + parser.timesToString(times))
									classTime = minTime(times[2], times[3]) - minTime(times[0], times[1])
									if classTime <= 0:
										print(str(classTime) + "-minute class on " + weekday + " in " + roomNum + " " + building + " at " + parser.timesToString(times))
										print("\tClass will not be included in classDict in any capacity")
										continue
									elif classTime < 50 or classTime > 300:
										print(str(classTime) + "-minute class on " + weekday + " in " + roomNum + " " + building + " at " + parser.timesToString(times))
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
