import string
import logging
import threading

from Socket import openSocket, sendWhisper, sendMessage
from Parse import parseMessage
from Config import CHAN, modlist
from ManageCmds import addcom, delcom, enablecom, disablecom, runcom
from threading import Thread
from CreateLogger import createlogger
from Uptime import updateuptime, getuptime, getdowntime
from Cooldown import cooldown
from Animals import getbun, addbun, getcat, addcat

chatLog = createlogger('Chat Log', 'Chat', '#'+CHAN, logging.INFO)
commandsLog = createlogger('Command Usage', 'Commands', '#'+CHAN, logging.INFO)
wcommandsLog = createlogger('Command Usage', 'Commands', 'Whispers', logging.INFO)


def connect():
	global s
	s = openSocket()

readbuffer = ""


def housekeeping():
	threading.Timer(600.0, housekeeping).start()
	# rank update goes here
	try:
		s.send('CAP\r\n')  # pseudo keep-alive (twitch sux)
	except:
		connect()

housekeeping()


def uptime():
	threading.Timer(30.0, uptime).start()
	updateuptime()

uptime()


class consoleInput(Thread):
	def run(self):
		while True:
			chatmessage = raw_input(':')
			sendMessage(s, chatmessage)

consoleInput().start()

while True:
	readbuffer = readbuffer + s.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()
	
	for line in temp:
		print(line)
		chatLog.info(line)
		if line.startswith("PING "):
			s.send("PONG tmi.twitch.tv\r\n")
			print("PONG!")
			break
		user, message, wuser, wmessage = parseMessage(line)

		try:
			if line.split(" ")[2] == "USERNOTICE":
				if line.split("msg-id=")[1].split(";")[0] == "sub":
					subber = line.split("display-name=",1)[1].split(";", 1)[0]
					if subber == "":
						subber = line.split("login=", 1)[1].split(";", 1)[0]
					sendMessage(s, "starB Gottem! Thanks for subscribing, "+subber+"! starB")
				elif line.split("msg-id=")[1].split(";")[0] == "resub":
					subber = line.split("display-name=", 1)[1].split(";", 1)[0]
					if subber == "":
						subber = line.split("login=", 1)[1].split(";", 1)[0]
					months = line.split("msg-param-months=")[1].split(";")[0]
					sendMessage(s, "starB Gottem! Thanks for resubbing for "+months+" months in a row, "+subber+"! starB")
		except IndexError:
			pass

		if user != "" and message != "":
			print(user + ": " + message)
			if message[0] is "!":
				cmd = message.split(" ", 1)[0][1:].strip("\r").lower()
				commandsLog.info(user + ' tried ' + message)
				if cmd == "addcom":
					if user not in modlist:
						break
					sendMessage(s, addcom(message, user))
				elif cmd == "delcom":
					if user not in modlist:
						break
					sendMessage(s, delcom(message, user))
				elif cmd == "enablecom":
					if user not in modlist:
						break
					sendMessage(s, enablecom(message, user))
				elif cmd == "disablecom":
					if user not in modlist:
						break
					sendMessage(s, disablecom(message, user))
				elif cmd == "bunny":
					if cooldown("!bunny", 15):
						break
					sendMessage(s, getbun())
				elif cmd == "addbun":
					if user not in modlist:
						break
					addbun(" ".join(message.split(" ")[1:]))
				elif cmd == "cat":
					if cooldown("!cat", 15):
						break
					sendMessage(s, getcat())
				elif cmd == "addcat":
					if user not in modlist:
						break
					addcat(" ".join(message.split(" ")[1:]))
				elif cmd == "uptime":
					if cooldown("!uptime", 15):
						break
					upt = getuptime()
					if upt is not None:
						sendMessage(s, "Ster has been live for "+upt+" starB")
					else:
						sendMessage(s, "Ster is currently offline.")
				elif cmd == "downtime":
					if cooldown("!downtime", 15):
						break
					dtm = getdowntime()
					if dtm is not None:
						sendMessage(s, "Ster has been offline for "+dtm+".")
				else:
					sendMessage(s, runcom(cmd, user))
