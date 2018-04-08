import datetime
from Functionality import readapi, ftime

offline = 0
startTime = None
uptime = None
endTime = None
length = None


def updateuptime():
	global startTime, offline, uptime, endTime, length
	if readapi('http://Burgtown.azurewebsites.net/php/online.php?user=skip_', 1) == "true":
		if startTime is None:
			startTime = datetime.datetime.now().replace(microsecond=0)
			offline = 0
			return True
		else:
			return False
	else:
		if startTime is not None and offline < 8:
			offline += 1
		elif offline == 8:
			length = ftime(str(datetime.datetime.now().replace(microsecond=0) - startTime))
			startTime = None
			offline = 0
			endTime = datetime.datetime.now().replace(microsecond=0)
		else:
			return


def getuptime():
	if startTime is not None:
		difference = str(datetime.datetime.now().replace(microsecond=0) - startTime)
		return ftime(difference)
	else:
		return


def getdowntime():
	if startTime is None and endTime is not None:
		difference = str(datetime.datetime.now().replace(microsecond=0) - endTime)
		return ftime(difference)
	else:
		return
