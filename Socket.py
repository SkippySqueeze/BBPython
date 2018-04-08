import socket
import random
from Config import HOST, PORT, NICK, PASS, CHAN


def openSocket():
	s = socket.socket()
	s.connect((HOST, PORT))
	s.send("CAP REQ :twitch.tv/tags\r\n")
	s.send("CAP REQ :twitch.tv/commands\r\n")
	s.send("CAP REQ :twitch.tv/membership\r\n")
	s.send("PASS " + PASS + "\r\n")
	s.send("NICK " + NICK + "\r\n")
	s.send("JOIN #" + CHAN + "\r\n")
	return s


def sendMessage(s, message):
	if message is None:
		print "Failed to send message"
		return
	messageTemp = "PRIVMSG #" + CHAN + " :" + message
	# randoColor(s)
	s.send(messageTemp + "\r\n")
	print("Sent: " + messageTemp)


def sendWhisper(s, TARGET, message):
	if message is None:
		# print "Failed to send whisper"
		return
	messageTemp = "PRIVMSG #burgahbot :/w " + TARGET + " " + message
	s.send(messageTemp + "\r\n")
	print("Sent: " + messageTemp)


def randoColor(s):
	color = hex(random.randint(0, 16777215))[2:].upper()
	s.send("PRIVMSG #" + CHAN + " :.color #" + color + "\r\n")
