

def parseMessage(line):
	usr=msg=wusr=wmsg=""
	try:
		if "PRIVMSG" in line.split("tmi.twitch.tv ", 1)[1].split(" ", 1)[0]:
			usr = line.split("display-name=",1)[1].split(";", 1)[0].lower()
			msg = line.split("PRIVMSG", 1)[1].split(":", 1)[1].strip('\r')
	except IndexError:
		pass
	try:
		if "WHISPER" in line.split("tmi.twitch.tv ", 1)[1].split(" ", 1)[0]:
			wusr = line.split("display-name=", 1)[1].split(";", 1)[0].lower()
			wmsg = line.split("tmi.twitch.tv ", 1)[1].split(":", 1)[1].strip('\r')
	except IndexError:
		pass
	return usr, msg, wusr, wmsg
