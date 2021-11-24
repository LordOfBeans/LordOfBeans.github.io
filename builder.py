import scraper
import datetime
import parser
import json

startDate = datetime.date(2021, 8, 27)
endDate = datetime.date(2021, 12, 19)

def buildRoomDict():
	roomDict = {}
	for subject in scraper.getClasses():
		for cls in subject:
			for i in range(0,len(cls[0])):
				if (cls[0][i] != None and cls[2][i] != None):
					if (cls[2][i] in roomDict):
						roomDict[cls[2][i]] += getDates(cls[0][i], cls[1][i])
					else:
						roomDict[cls[2][i]] = getDates(cls[0][i], cls[1][i])
	return roomDict

def getDates(days, dates):
	ret = []
	startTime = datetime.time(days[1][0], days[1][1])
	endTime = datetime.time(days[2][0], days[2][1])
	end = datetime.date(dates[1][2], dates[1][0], dates[1][1])
	for day in days[0]:
		curr = datetime.date(dates[0][2], dates[0][0], dates[0][1])
		while(curr <= end and day!= curr.weekday()):
			curr += datetime.timedelta(1)
		while(curr <= end):
			ret.append([datetime.datetime.combine(curr, startTime), datetime.datetime.combine(curr, endTime)])
			curr += datetime.timedelta(7)
	return ret

def sortedRoomDict():
	roomDict = buildRoomDict()
	for classes in roomDict.values():
		classes.sort(key = lambda x: x[0])
	print("Number of classrooms: " + str(len(roomDict)))
	return roomDict

def buildingDict():
	buildingDict = {}
	roomDict = sortedRoomDict()
	for cls in roomDict.items():
		building = parser.parseBuilding(cls[0])
		if building[0] in buildingDict:
			buildingDict[building[0]][building[1]] = cls[1]
		else:
			buildingDict[building[0]] = {building[1]:cls[1]}
	return buildingDict

def getBuildingHours(building, weekday):
	if building == 'Information Sciences Building' or building == 'Sennott Square':
		if weekday <= 3:
			return [datetime.time(7), datetime.time(22)]
		elif weekday == 4:
			return [datetime.time(7), datetime.time(18)]
		elif weekday == 5:
			return [datetime.time(8,30), datetime.time(18)]
		else:
			return None
	elif building == 'Music Building':
		if weekday <= 3:
			return [datetime.time(8,30), datetime.time(20,45)]
		elif weekday == 4:
			return [datetime.time(8,30), datetime.time(17)]
		else:
			return None
	elif building == 'Cathedral of Learning':
		if weekday <= 4:
			return [datetime.time(7), datetime.time(23)]
		else:
			return [datetime.time(7,30), datetime.time(23)]
	elif building == 'Benedum Hall':
		if weekday <= 4:
			return [datetime.time(7,30), datetime.time(22)]
		else:
			return [datetime.time(8), datetime.time(22)]
	elif building == 'Lawrence Hall':
		if weekday <= 4:
			return [datetime.time(7,30), datetime.time(22)]
		else:
			return [datetime.time(8), datetime.time(20)]
	elif building == 'Frick Fine Arts Builing':
		if weekday <= 4:
			return [datetime.time(7,30), datetime.time(22)]
		else:
			return [datetime.time(10), datetime.time(18)]
	elif building == 'Posvar Hall':
		if weekday <= 4:
			return [datetime.time(7,30), datetime.time(22)]
		else:
			return [datetime.time(8), datetime.time(20)]
	else:
		if weekday <= 4:
			return [datetime.time(7,30), datetime.time(22)]
		else:
			return None

def roomOpenings():
	roomOpenings = {}
	for building in buildingDict().items():
		for cls in building[1].items():
			curr = startDate
			index = 0
			while (curr <= endDate):
				hours = getBuildingHours(building[0], curr.weekday())
				if hours == None:
					curr += datetime.timedelta(1)
					continue
				currTime = datetime.datetime.combine(curr,hours[0])
				while index < len(cls[1]) and currTime.date() == cls[1][index][0].date():
					open = openTime(currTime, cls[1][index][0])
					if open != None:
						if building[0] in roomOpenings:
							if cls[0] in roomOpenings[building[0]]:
								roomOpenings[building[0]][cls[0]].append(open)
							else:
								roomOpenings[building[0]][cls[0]] = [open]
						else:
							roomOpenings[building[0]] = {cls[0]:[open]}
					currTime = cls[1][index][1]
					index += 1
				open = openTime(currTime, datetime.datetime.combine(curr,hours[1]))
				if open != None:
					if building[0] in roomOpenings:
						if cls[0] in roomOpenings[building[0]]:
							roomOpenings[building[0]][cls[0]].append(open)
						else:
							roomOpenings[building[0]][cls[0]] = [open]
					else:
						roomOpenings[building[0]] = {cls[0]:[open]}
				curr += datetime.timedelta(1)
	return roomOpenings

			
# returns the opening in time if at least 60 minutes of time are available
def openTime(start, end):
	openTime = end.hour*60 - start.hour*60 + end.minute - start.minute
	if openTime >= 60:
		return [start, end]
	else:
		return None

def openingList():
	openingList = []
	openings = roomOpenings()
	for building in openings.items():
		for room in building[1].items():
			for opening in room[1]:
				openingList.append([building[0], room[0], opening])
	openingList.sort(key = lambda x: (x[2][0], x[2][1], x[0], x[1]))
	return openingList

#Used for sorting by time in openList2
def startNum(arr):
	return arr[0] * 535,680 + arr[1] * 44640 + arr[2] * 1440 + arr[3] * 60 + arr[4]
	

def openList2():
	openList = []
	openings = roomOpenings()
	for building in openings.items():
		for room in building[1].items():
			for times in room[1]:
				start = times[0]
				end = times[1]
				openList.append([building[0], room[0], [start.year, start.month, start.day, start.hour, start.minute], [end.year, end.month, end.day, end.hour, end.minute]])
	return sorted(openList, key = lambda x: (startNum(x[2]), x[0], x[1]))

def printOpenings(openings):
	index = 0
	currDate = startDate 
	while currDate <= endDate:
		print("Date: " + str(currDate.month) + "/" + str(currDate.day) + "/" + str(currDate.year))
		while index < len(openings) and openings[index][2][0].date() == currDate:
			opening = openings[index]
			start = opening[2]
			print("\t" + opening[1] + " " + opening[0] + ": " + str(opening[2][0].hour) + ":" + str(opening[2][0].minute) + " to " + str(opening[2][1].hour) + ":" + str(opening[2][1].minute))
			index += 1
		currDate += datetime.timedelta(1)

def buildJson(openings):
	index = 0
	openingJson = {}
	for cls in openings:
		date = cls[2][0].strftime("%A %B %d, %Y") 
		start = cls[2][0].strftime("%I:%M %p")
		end = cls[2][1].strftime("%I:%M %p")
		building = cls[0]
		room = cls[1]
		if date in openingJson:
			if building in openingJson[date]:
				if room in openingJson[date][building]:
					openingJson[date][building][room].append({"start":start, "end":end})
				else:
					openingJson[date][building][room] = [{"start":start,"end":end}]
			else:
				openingJson[date][building] = {room:[{"start":start,"end":end}]}
		else:
			openingJson[date] = {building: {room:[{"start":start,"end":end}]}}
	with open("openings.json","w") as jFile:
		json.dump(openingJson, jFile)

def printFromJson(fileName):
	with open(fileName) as jsonFile:
		openings = json.load(jsonFile)
	for date in openings.items():
		print("# " + date[0] + ":")
		for building in sorted(list(date[1].items()), key = lambda x: x[0]):
			print("> ## " + building[0] + ":")
			for room in sorted(list(building[1].items()), key = lambda y: y[0]):
				newString = "> > " + room[0] + ": "
				for time in room[1]:
					newString += time["start"] + " - " + time["end"] + " | "
				print(newString[:-3])

def toJsonFile(data, fileName):
	with open(fileName,"w") as jFile:
		json.dump(data, jFile)	
		
	