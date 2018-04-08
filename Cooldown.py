from threading import Timer

cooldowns = []
usercooldowns = []
disabled = []


def cooldown(cmd, cd):
	if cmd in cooldowns:
		print 'Cooldown for ' + cmd
		return True
	if cmd in disabled:
		print cmd + ' disabled'
		return True
	cooldowns.append(cmd)
	a = Timer(cd, removecd, [cmd])
	a.start()
	print 'Starting cooldown for ' + cmd
	return False


def removecd(cmd):
	if cmd in cooldowns:
		print 'Cooldown ended for ' + cmd
		cooldowns.remove(cmd)
	else:
		return


def wcooldown(wuser, cmd, cd):
	if wuser in usercooldowns:
		print 'Whisper cooldown for ' + wuser
		return True
	if cmd in disabled:
		print 'Command "' + cmd + '" disabled'
		return True
	usercooldowns.append(wuser)
	b = Timer(cd, removeuser, [wuser])
	b.start()
	print 'Starting whisper cooldown for ' + wuser
	return False


def removeuser(wuser):
	if wuser in usercooldowns:
		print 'Whisper cooldown ended for ' + wuser
		usercooldowns.remove(wuser)
	else:
		return


def disable(cmd):
	if 'commands.' + cmd in disabled:
		print 'Command ' + 'commands.' + cmd + ' already disabled'
		return False
	disabled.append('commands.' + cmd)
	print 'Command ' + 'commands.' + cmd + ' disabled'
	return True


def enable(cmd):
	if 'commands.' + cmd in disabled:
		disabled.remove('commands.' + cmd)
		print 'Command ' + 'commands.' + cmd + ' enabled'
		return True
	else:
		return False
