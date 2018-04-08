import urllib2
import datetime


def readapi(url, lines):
	try:
		request = urllib2.Request(url.lower(), headers={"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": "client_id_here"})
		contents = urllib2.urlopen(request).read()
		return contents.split("\n")[lines - 1]
	except urllib2.URLError as e:
		print e
		print url
		return "Error opening URL"


def countdown(date):
	currenttime = datetime.datetime.now().replace(microsecond=0)
	futuretime = datetime.datetime.strptime(date, "%m/%d/%y_%H:%M:%S")
	difference = str(futuretime - currenttime)
	return ftime(difference)


def ftime(difference):
	formattime = None
	try:
		fminutes = difference.split(":")[1]
	except IndexError:
		pass

	try:
		fhours = difference.split(":")[0].split(", ")[1]
	except IndexError:
		fhours = difference.split(":")[0]

	if "day" in difference:
		fdays = difference.split(", ")[0]
	else:
		fdays = None

	if fminutes != "00":
		if fminutes[0] == "0":
			if fminutes[1] == "1":
				formattime = fminutes[1] + " minute"
			else:
				formattime = fminutes[1] + " minutes"
		else:
			formattime = fminutes + " minutes"

	if fhours != "0":
		if formattime is not None:
			if fhours == "1":
				formattime = fhours + " hour and " + formattime
			else:
				formattime = fhours + " hours and " + formattime
		else:
			if fhours == "1":
				formattime = fhours + " hour"
			else:
				formattime = fhours + " hours"

	if fdays is not None:
		if formattime is not None:
			if fminutes != "00" and fhours != "0":
				formattime = fdays + ", " + formattime
			else:
				formattime = fdays + " and " + formattime
		else:
			formattime = fdays

	if formattime is None:
		formattime = "<1 minute"

	return formattime


def gettime():
	currenttime = '{0:%I:%M %p}'.format(datetime.datetime.now())
	return currenttime
