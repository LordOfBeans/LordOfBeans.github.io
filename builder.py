import scraper
import datetime
import parser
import json

def toJsonFile(data, fileName):
	with open(fileName, "w") as jFile:
		json.dump(data, jFile)

toJsonFile(scraper.buildClassDict(), "classDict.json")