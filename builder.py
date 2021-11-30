import scraper
import datetime
import parser
import json

#MIN_TIME is the minimum amount of time necessary for an opening to be considered worthy of inclusion as a study space
MIN_TIME = 60

def setJsonFile(data, fileName):
	with open(fileName, "w") as jFile:
		json.dump(data, jFile)

def getJsonFile(fileName):
	with open(fileName) as jFile:
		data = json.load(jFile)
	return data

def checkOpening(start, end):
	delta = scraper.minTime(end[0], end[1]) - scraper.minTime(start[0], start[1])
	if delta >= MIN_TIME:
		return True
	else:
		return False

def placeOpening(openDict, weekday, building, room, opening):
	if weekday in openDict.keys():
		if building in openDict[weekday].keys():
			if room in openDict[weekday][building].keys():
				openDict[weekday][building][room].append(opening)
			else:
				openDict[weekday][building][room] = [opening]
		else:
			openDict[weekday][building] = {room:[opening]}
	else:
		openDict[weekday] = {building:{room:[opening]}}

def addRoom(closedDict, weekday, building, room):
	if weekday in closedDict.keys():
		if building in closedDict[weekday].keys():
			if room in closedDict[weekday][building].keys():
				return
			else:
				closedDict[weekday][building][room] = []
		else:
			if parser.getBuildingHours(building, weekday) != None:
				closedDict[weekday][building] = {room:[]}
	else:
		if parser.getBuildingHours(building, weekday) != None:
			closedDict[weekday] = {building:{room:[]}}
			
	

def buildOpeningDict():
	data = getJsonFile("classDict.json")
	openDict = {}
	for weekday in data.items():
		for weekday2 in data.items():
			for building in weekday2[1].items():
				for room in building[1].items():
					addRoom(data, weekday[0], building[0], room[0])
		for building in weekday[1].items():
			hours = parser.getBuildingHours(building[0], weekday[0])
			for room in building[1].items():
				start = hours[:2]
				for closed in room[1]:
					end = closed[:2]
					if checkOpening(start, end):
						placeOpening(openDict, weekday[0], building[0], room[0], [start[0], start[1], end[0], end[1]])
					start = closed[2:]
				end = hours[2:]
				if checkOpening(start, end):
					placeOpening(openDict, weekday[0], building[0], room[0], [start[0], start[1], end[0], end[1]])
	return openDict

def openingsToHTML(fileName):
	openDict = getJsonFile("openDict.json")
	html = ""
	for weekday in openDict.items():
		html += "<div class=\"weekday item\"><div class=\"name\">" + weekday[0] + "</div><div class=\"container\">"
		for building in weekday[1].items():
			html += "<div class=\"building item\"><div class=\"name\">" + building[0] + "</div><div class=\"rooms\">"
			for room in building[1].items():
				roomString = ""
				for opening in room[1]:
					roomString += parser.timesToString(opening) + " | "
				html += "<b>" + room[0] + ": </b>" + roomString[:-3] + "<br>"
			html += "</div></div>"
		html += "</div></div>"
	with open(fileName, "w") as htmlFile:
		htmlFile.write(html)
	
openingsToHTML("open.html")
				