#returns start and end time as list of tuples
def parseTimes(str):
	times = str.split(' - ')
	ret = []
	for time in times:
		hour = int(time[:-5])
		if hour == 12:
			hour = 0
		minute = int(time[-4:-2])
		if (time[-2:] == 'pm'):
			ret.append([hour+12,minute])
		else:
			ret.append([hour,minute])
	return ret

#returns list with days as integers and start and end times as integers
def parseDay(str):
	index = 0
	ret = [[]]
	while (str[index] != ' '):
		abr_day = str[index:index+2]
		if (abr_day == 'Mo'):
			ret[0].append(0)
		elif (abr_day == 'Tu'):
			ret[0].append(1)
		elif (abr_day == 'We'):
			ret[0].append(2)
		elif (abr_day == 'Th'):
			ret[0].append(3)
		elif (abr_day == 'Fr'):
			ret[0].append(4)
		elif (abr_day == 'Sa'):
			ret[0].append(5)
		index+=2
	ret += (parseTimes(str[index+1:]))
	return ret

def parseDays(str):
	ret = []
	for day in str.split(', '):
		if (day == 'TBA'):
			ret.append(None)
		else:
			ret.append(parseDay(day))
	return ret

def parseDate(str):
	dates = str.split(' - ')
	ret = []
	for date in dates:
		month = int(date[0:2])
		day = int(date[3:5])
		year = int(date[6:])
		ret.append([month, day, year])
	return ret

def parseDates(str):
	ret = []
	for date in str.split(', '):
		ret.append(parseDate(date))
	return ret

def parseRooms(str):
	ret = []
	for room in str.split(', '):
		if (room == 'TO BE ARRANGED' or room == 'WEB Based Class' or room == 'TBA' or room == 'OFF CAMPUS TO BE ARRANGED'):
			ret.append(None)
		else:
			ret.append(room)
	return ret

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
		return ['Trees Hall', room[:-11]]
	elif (room[-15:] == ' Music Building'):
		return ['Music Building', room[:-15]]
	elif (room[-16:] == ' Bellefield Hall'):
		return ['Bellefield Hall', room[:-16]]
	elif (room[-13:] == ' Forbes Tower'):
		return ['Forbes Tower', room[:-13]]
	elif (room[-12:] == ' Mervis Hall'):
		return ['Mervis Hall', room[:-12]]
	elif (room[-18:] == ' Parkvale Building'):
		return ['Parkvale Building', room[:-18]]
	elif (room[-27:] == ' Gardner Steel Conf  Center'):
		return ['Gardner Steel Conference Center', room[:-27]]
	elif (room[-19:] == ' Barco Law Building'):
		return ['Barco Law Building', room[:-19]]
	elif (room[-19:] == ' William Pitt Union'):
		return ['William Pitt Union', room[:-19]]
	elif (room[-20:] == ' The Offices at Baum'):
		return ['The Offices at Buam', room[:-20]]
	elif (room[-11:] == ' Clapp Hall'):
		return ['Clapp Hall', room[:-11]]
	elif (room[-11:] == ' Bruce hall'):
		return ['Bruce Hall', room[:-11]]
	elif (room[-10:] == ' Salk Hall'):
		return ['Salk Hall', room[:-10]]
	elif (room[-5:] == ' BST3'):
		return ['Biomedial Science Tower 3', room[:-5]]
	elif (room[-17:] == ' Murdoch Building'):
		return ['Murdoch Building', room[:-17]]
	elif (room[-19:] == ' 3343 Forbes Avenue'):
		return ['3343 Forbes Avenue', room[:-19]]
	elif (room[-22:] == ' O\'Hara Student Center'):
		return ['O\'Hara Student Center', room[:-22]]
	elif (room[-27:] == ' Space Res Coordination Cen'):
		return ['Space Research Coordination Center', room[:-27]]
	elif (room[-25:] == ' Biomedical Science Tower'):
		return ['Bomedical Science Tower', room[:-25]]
	elif (room[-17:] == ' Mellon Institute'):
		return ['Mellon Institute', room[:-17]]
	elif (room[-12:] == ' Swarts Hall'):
		return ['Swarts Hall', room[:-12]]
	elif (room[-26:] == ' Sports and Fitness Center'):
		return ['Sports and Fitness Center', room[:-26]]
	elif (room[-11:] == ' Salk Annex'):
		return ['Salk Annex', room[:-11]]
	elif (room[-12:] == ' Scaife Hall'):
		return ['Scaife Hall', room[:-12]]
	elif (room[-20:] == ' Bridgeside Point II'):
		return ['Bridgeside Point II', room[:-20]]
	elif (room == 'THAW 00207'):
		return ['Thaw Hall', '207']
	else:
		return [room,'']
		