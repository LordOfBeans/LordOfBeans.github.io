#returns start and end time as [start_hour, start_min, end_hour, end_min]
#ex: [8, 0, 9, 15] = class occurs from 8:00 AM to 9:15 AM
def parseTimes(str):
	times = str.split(' - ')
	ret = []
	for time in times:
		hour = int(time[:-5])
		if hour == 12:
			hour = 0
		minute = int(time[-4:-2])
		if (time[-2:] == 'pm'):
			ret += [hour+12,minute]
		else:
			ret += [hour,minute]
	return ret

#returns list with days as nested list and times as last 4 indexes, which are returned by parseTimes
#ex: [["Tuesday", "Thursday"], 8, 0, 9, 15] = class occurs Tuesdays and Thursdays from 8:00 AM to 9:15 AM
def parseDay(str):
	index = 0
	ret = [[]]
	while (str[index] != ' '):
		abr_day = str[index:index+2]
		if (abr_day == 'Mo'):
			ret[0].append("Monday")
		elif (abr_day == 'Tu'):
			ret[0].append("Tuesday")
		elif (abr_day == 'We'):
			ret[0].append("Wednesday")
		elif (abr_day == 'Th'):
			ret[0].append("Thursday")
		elif (abr_day == 'Fr'):
			ret[0].append("Friday")
		elif (abr_day == 'Sa'):
			ret[0].append("Saturday")
		index+=2
	ret += parseTimes(str[index+1:])
	return ret

#Returns list of lists returned by parseDay or None if day is invalid
#Should be same length as list returned by parseRooms and something has gone wrong if not
def parseDays(str):
	ret = []
	for day in str.split(', '):
		if (day == 'TBA'):
			ret.append(None)
		else:
			ret.append(parseDay(day))
	return ret

#Returns a list of lists returned by parseBuilding or None if room is invalid
def parseRooms(str):
	ret = []
	for room in str.split(', '):
		roomArr = parseBuilding(room)
		ret.append(roomArr)
	return ret

#Returns a list with the name of the building as the first index and the room number as the second
#Returns a list with an empty second index if it cannot parse
#Returns None for quite a few places, which effectively ignores them, because I don't know th buildings well and they only have a few open rooms
def parseBuilding(room):
	if (room[-21:] == ' Wesley W Posvar Hall'):
		return ['Posvar Hall', room[:-21]]
	elif (room[-22:] == ' Cathedral of Learning'):
		return ['Cathedral of Learning', room[:-22]]
	elif (room[-23:] == ' Chevron Science Center'):
		return ['Chevron Science Center', room[:-23]]
	elif (room[-25:] == ' Frick Fine Arts Building'):
		return ['Frick Fine Arts Building', room[:-25]]
	elif (room [-14:] == ' Lawrence Hall'):
		return ['Lawrence Hall', room[:-14]]
	elif (room [-13:] == ' Benedum Hall'):
		return ['Benedum Hall', room[:-13]]
	elif (room [-18:] == ' Victoria Building'):
		return ['Victoria Building', room[:-18]]
	elif (room [-13:] == ' Langley Hall'):
		return ['Langley Hall', room[:-13]]
	elif (room [-14:] == ' Public Health'):
		return ['Public Health Building', room[:-14]]
	elif (room[-23:] == ' Public Health-Crabtree'):
		return ['Public Health-Crabtree', room[:-23]]
	elif (room[-21:] == ' Old Engineering Hall'):
		return ['Old Engineering Hall', room[:-21]]
	elif (room[-27:] == ' Information Sciences Build'):
		return ['Information Sciences Building', room[:-27]]
	elif (room[-15:] == ' Sennott Square'):
		return ['Sennott Square', room[:-15]]
	elif (room[-15:] == ' Thackeray Hall'):
		return ['Thackeray Hall', room[:-15]]
	elif (room[-24:] == ' Alexander J. Allen Hall'):
		return ['Allen Hall', room[:-24]]
	elif (room[-10:] == ' Thaw Hall'):
		return ['Thaw Hall', room[:-10]]
	elif (room[-14:] == ' Crawford Hall'):
		return ['Crawford Hall', room[:-14]]
	elif (room[-12:] == ' Eberly Hall'):
		return ['Eberly Hall', room[:-12]]
	elif (room[-12:] == ' Alumni Hall'):
		return ['Alumni Hall', room[:-12]]
	elif (room[-11:] == ' Trees Hall'):
		return None
	elif (room[-15:] == ' Music Building'):
		return ['Music Building', room[:-15]]
	elif (room[-16:] == ' Bellefield Hall'):
		return None
	elif (room[-13:] == ' Forbes Tower'):
		return ['Forbes Tower', room[:-13]]
	elif (room[-12:] == ' Mervis Hall'):
		return ['Mervis Hall', room[:-12]]
	elif (room[-18:] == ' Parkvale Building'):
		return None
	elif (room[-27:] == ' Gardner Steel Conf  Center'):
		return None
	elif (room[-19:] == ' Barco Law Building'):
		return ['Barco Law Building', room[:-19]]
	elif (room[-19:] == ' William Pitt Union'):
		return None
	elif (room[-20:] == ' The Offices at Baum'):
		return None
	elif (room[-11:] == ' Clapp Hall'):
		return ['Clapp Hall', room[:-11]]
	elif (room[-11:] == ' Bruce hall'):
		return None
	elif (room[-10:] == ' Salk Hall'):
		return ['Salk Hall', room[:-10]]
	elif (room[-5:] == ' BST3'):
		return None
	elif (room[-17:] == ' Murdoch Building'):
		return None
	elif (room[-19:] == ' 3343 Forbes Avenue'):
		return None
	elif (room[-22:] == ' O\'Hara Student Center'):
		return None
	elif (room[-27:] == ' Space Res Coordination Cen'):
		return None
	elif (room[-25:] == ' Biomedical Science Tower'):
		return None
	elif (room[-17:] == ' Mellon Institute'):
		return None
	elif (room[-12:] == ' Swarts Hall'):
		return None
	elif (room[-26:] == ' Sports and Fitness Center'):
		return None
	elif (room[-11:] == ' Salk Annex'):
		return None
	elif (room[-12:] == ' Scaife Hall'):
		return None
	elif (room[-20:] == ' Bridgeside Point II'):
		return None
	elif (room == 'THAW 00207'):
		return ['Thaw Hall', '207']
	else:
		return None

#This could probably be written better at this point
def getBuildingHours(building, weekday):
	if building == 'Information Sciences Building' or building == 'Sennott Square':
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday":
			return [7, 0, 22, 0]
		elif weekday == "Friday":
			return [7, 0, 18, 0]
		elif weekday == "Saturday":
			return [8, 30, 18, 0]
		else:
			return None
	elif building == 'Music Building':
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday":
			return [8, 30, 20, 45]
		elif weekday == "Friday":
			return [8, 30, 17, 0]
		else:
			return None
	elif building == 'Cathedral of Learning':
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday" or weekday == "Friday":
			return [7, 0, 23, 0]
		else:
			return [7, 30, 23, 0]
	elif building == 'Benedum Hall':
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday" or weekday == "Friday":
			return [7, 30, 22, 0]
		else:
			return [8, 0, 22, 0]
	elif building == 'Lawrence Hall':
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday" or weekday == "Friday":
			return [7, 30, 22, 0]
		else:
			return [8, 0, 20, 0]
	elif building == 'Frick Fine Arts Builing':
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday" or weekday == "Friday":
			return [7, 30, 22, 0]
		else:
			return [10, 0, 18, 0]
	elif building == 'Posvar Hall':
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday" or weekday == "Friday":
			return [7, 30, 22, 0]
		else:
			return [8, 0, 20, 0]
	else:
		if weekday == "Monday" or weekday == "Tuesday" or weekday == "Wednesday" or weekday == "Thursday" or weekday == "Friday":
			return [7, 30, 22, 0]
		else:
			return None

def timeToString(hour, minute):
	if hour >= 12:
		period = "PM"
		hour -= 12
	else:
		period = "AM"
	if hour == 0:
		hour = 12
	if minute < 10:
		return str(hour) + ":0" + str(minute) + " " + period
	else:
		return str(hour) + ":" + str(minute) + " " + period

def timesToString(arr):
	return timeToString(arr[0], arr[1]) + " - " + timeToString(arr[2], arr[3])

def timeReplace(arr, i1, i2, time):
	for i in range(i1 + 1, i2):
		arr.pop(i)
	arr[i1] = time
	