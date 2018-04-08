HOST = "irc.twitch.tv"
PORT = 6667
NICK = "burgahbot"
PASS = "oauth:token"
CHAN = "skip_"
modlist = [x.strip() for x in open("modlist.txt").readlines()]
