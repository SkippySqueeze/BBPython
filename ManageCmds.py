import sys
import logging
import time
import MySQLdb
from Config import modlist
from CreateLogger import createlogger
from Cooldown import cooldown
from Functionality import *

cmdLog = createlogger('Command Manager Log', 'CmdManagement', time.strftime('%d-%m-%Y'), logging.DEBUG)

db = MySQLdb.connect("localhost", "bb", "password", "burgahbot")
cursor = db.cursor()


def addcom(msg, user):
	if user not in modlist:
		cmdLog.debug('Failed to create command. No permission. User: ' + user)
		return
	try:
		msg = msg.strip('\n')
		cmdLog.debug('Creating initial split.')
		c = msg.split(" ", 1)[1]
		if c[0] is '!':
			try:
				# Get command name
				newcmd = c.split(' ', 1)[0][1:].lower()
				cmdLog.debug('Name: '+newcmd)

				# Check if it exists already
				sql = "SELECT NAME FROM COMMANDS \
					   WHERE NAME = %s"
				cursor.execute(sql, (newcmd,))
				commandname = cursor.fetchone()
				if commandname is not None:
					cmdLog.debug(newcmd+' exists. Creation failed.')
					return "Command !"+newcmd+" already exists. starB"

				# Check if the command body exists
				if not c.split(' ', 1)[1:]:
					cmdLog.debug('No command body. Creation failed.')
					return "Could not create command, please refer to the guide: !bbhelp starB"

				# Create body string
				cmdLog.debug('Creating command body var.')
				cmdout = ' '.join(c.split(' ', 1)[1:])
				cmdoutlist = cmdout.split(' ')

				# Check for flags
				cooldown = 30
				modonly = False
				offlineonly = False
				deletable = True
				if cmdoutlist[0].startswith('-'):
					flags = cmdoutlist[0].strip('-')
					cmdout = cmdout.split(' ', 1)[1]
					if 'm' in flags:
						modonly = True
						flags = flags.strip('m')
					if 'o' in flags:
						offlineonly = True
						flags = flags.strip('o')
					if 'u' in flags:
						if user == 'skippysqueeze':
							deletable = False
						flags = flags.strip('u')
					if 'c' in flags:
						flags = flags.strip('c')
						cooldown = flags
				if cooldown > 86400:
					cooldown = 86400
				if cooldown < 10:
					cooldown = 10

				# Write the command to the DB
				sql = "INSERT INTO COMMANDS(NAME, \
						 TEXT, COOLDOWN, OFFLINE, \
					     MODERATOR, DELETABLE, DISABLED) \
						 VALUES (%s, %s, %s, %s, %s, %s, %s)"
				try:
					cursor.execute(sql, (newcmd, cmdout, cooldown, offlineonly, modonly, deletable, False))
					db.commit()
				except:
					cmdLog.debug(sys.exc_info()[0])
					db.rollback()
					print "COMMAND CREATION FAILED"

				# Let 'em know it's all alright
				cmdLog.debug('Command '+newcmd+' created successfully.')
				return "Successfully created command !"+newcmd+" starB"
			except IndexError:
				cmdLog.debug('Failed to create command. IndexError.')
				return "Could not create command, please follow the instructions from !bbhelp starB"
	except IndexError:
		cmdLog.debug('Failed to create command. IndexError.')
		return "Could not create command, please follow the instructions from !bbhelp starB"


def delcom(msg, user):
	cmdLog.debug('===============================')
	cmdLog.debug('Attempting command deletion.')
	if user not in modlist:
		cmdLog.debug('Failed to delete command. No permission. User: ' + user)
		return
	try:
		cmdLog.debug('Creating initial split.')
		c = msg.split(" ", 1)[1]
		if c[0] is '!':
			try:
				# Get command name
				delcmd = c.split(' ', 1)[0][1:].lower()
				if delcmd == 'addcom':
					return 'starBaka'
				cmdLog.debug('Name: '+delcmd)

				# Check if it exists
				sql = "SELECT * FROM COMMANDS \
					   WHERE NAME = %s"
				cursor.execute(sql, (delcmd,))
				cmdinfo = cursor.fetchone()
				if cmdinfo is None:
					cmdLog.debug('Command does not exist. Deletion failed.')
					return "Command !" + delcmd + " does not exist. starGorbo"

				# Check if it's deletable
				if cmdinfo[5] is 0:
					cmdLog.debug('Command is not flagged deletable. Deletion failed.')
					return "Command !" + delcmd + " is not deletable. starGorbo"

				# Remove command from cmdlist
				cmdLog.debug('Removing command from database')
				sql = "DELETE FROM COMMANDS \
					   WHERE NAME = %s"
				try:
					cursor.execute(sql, (delcmd,))
					db.commit()
				except:
					cmdLog.debug(sys.exc_info()[0])
					db.rollback()
					print "MESSAGE DELETION FAILED"

				# Let 'em know it's all alright
				cmdLog.debug('Command '+delcmd+' deleted successfully.')
				return "Successfully deleted command !" + delcmd + " starB"
			except IndexError:
				cmdLog.debug('Failed to delete command ' + delcmd + '. IndexError.')
				return "Could not delete command, please follow the instructions from !bbhelp starB"
	except IndexError:
		cmdLog.debug('Failed to delete command. IndexError.')
		return "Could not delete command, please follow the instructions from !bbhelp starB"


def enablecom(msg, user):
	cmdLog.debug('===============================')
	cmdLog.debug('Attempting to enable command')
	if user not in modlist:
		cmdLog.debug('User' + user + 'not in modlist')
		cmdLog.debug('Failed to enable command')
		return
	try:
		# Get command name
		cmd = msg.split(' ', 1)[1][1:].lower()
		cmdLog.debug('Name: ' + cmd)
	except IndexError:
		cmdLog.debug('Failed to enable command "' + cmd + '"')
		return 'Could not enable command, please follow the instructions from !bbhelp starB'
	sql = "SELECT DISABLED FROM COMMANDS \
		   WHERE NAME = %s"
	cursor.execute(sql, (cmd,))
	disabled = cursor.fetchone()
	if disabled is None:
		return
	if disabled[0] is 1:
		sql = "UPDATE COMMANDS \
			   SET DISABLED = 0 \
			   WHERE NAME = %s"
		try:
			cursor.execute(sql, (cmd,))
			db.commit()
			cmdLog.debug('Command "' + cmd + '" enabled')
			return 'Command "' + cmd + '" enabled starB'
		except:
			cmdLog.debug(sys.exc_info()[0])
			db.rollback()
			print "COMMAND ENABLING FAILED"
	else:
		cmdLog.debug('Failed to enable command "' + cmd + '"')
		return 'Command "' + cmd + '" is not disabled starB'


def disablecom(msg, user):
	cmdLog.debug('===============================')
	cmdLog.debug('Attempting to disable command')
	if user not in modlist:
		cmdLog.debug('User' + user + 'not in modlist')
		cmdLog.debug('Failed to disable command')
		return
	try:
		# Get command name
		cmd = msg.split(' ', 1)[1][1:].lower()
		cmdLog.debug('Name: ' + cmd)
	except IndexError:
		cmdLog.debug('Failed to disable command "' + cmd + '"')
		return 'Could not disable command, please follow the instructions from !bbhelp starB'
	sql = "SELECT DISABLED FROM COMMANDS \
			   WHERE NAME = %s"
	cursor.execute(sql, (cmd,))
	disabled = cursor.fetchone()
	if disabled is None:
		return
	if disabled[0] is 0:
		sql = "UPDATE COMMANDS \
			   SET DISABLED = 1 \
			   WHERE NAME = %s"
		try:
			cursor.execute(sql, (cmd,))
			db.commit()
			cmdLog.debug('Command "' + cmd + '" disabled')
			return 'Command "' + cmd + '" disabled starB'
		except:
			cmdLog.debug(sys.exc_info()[0])
			db.rollback()
			print "COMMAND DISABLING FAILED"
	else:
		cmdLog.debug('Failed to disable command "' + cmd + '"')
		return 'Command "' + cmd + '" is already disabled starB'


def runcom(cmd, user):
	sql = "SELECT * FROM COMMANDS \
			   WHERE NAME = %s"
	cursor.execute(sql, (cmd,))
	cmdinfo = cursor.fetchone()
	if cmdinfo is not None:
		if cmdinfo[6] is 1:
			return
		if cmdinfo[4] is 1:
			if user not in modlist:
				return
		cd = cmdinfo[2]
		if cooldown(cmd, cd):
			return
		retval = cmdinfo[1].split()
		for word in retval:
			if word[0] == ':' and word[-1] == ':':
				if ':user:' in word:
					retval[retval.index(word)] = retval[retval.index(word)].replace(':user:', user)
					word = word.replace(':user:', user)
				if word.strip(':') == 'gettime':
					retval[retval.index(':gettime:')] = gettime()
				elif 'readapi' in word.strip(':'):
					try:
						apiurl = word.split('(')[1].split(')')[0]
						retval[retval.index(word)] = readapi(apiurl, 1)
					except:
						retval[retval.index(word)] = '[error]'
				elif 'countdown' in word.strip(':'):
					try:
						future = word.split('(')[1].split(')')[0]
						retval[retval.index(word)] = countdown(future)
					except:
						retval[retval.index(word)] = '[error]'
		return ' '.join(retval)
	else:
		return
