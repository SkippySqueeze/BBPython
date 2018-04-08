from urllib2 import Request, urlopen, URLError


def getid(user):
	request = Request('http://burgtown.azurewebsites.net/php/get_id.php?user='+user)
	try:
		response = urlopen(request)
		api = response.read()
		return api[0:-1]
	except URLError, e:
		print "ERROR: ", e
		return 00000000
