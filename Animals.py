import sys
import MySQLdb
import urllib2

db = MySQLdb.connect("localhost", "bb", "password", "burgahbot")
cursor = db.cursor()


def getbun():
	sql = "SELECT url,id FROM buns WHERE used = 0 ORDER BY id ASC"
	try:
		cursor.execute(sql, ())
		data = cursor.fetchone()
		incbun(int(data[1]))
		return data[0]+" floootB"
	except:
		print sys.exc_info()[0]
		db.rollback()
		print "[DB ERROR] Can't get bun"
		return "Bunny dispenser empty. Please ask your bunny attendant to pour in more bun."


def incbun(id):
	sql = "UPDATE buns SET used = 1 WHERE used = 0 AND id = %s"
	try:
		cursor.execute(sql, (id, ))
		db.commit()
	except:
		print sys.exc_info()[0]
		db.rollback()
		print "[DB ERROR] Can't update bun"


def addbun(message):
	if message[0] == "-":
		try:
			albumurl = message.split(" ")[1]
			albumid = albumurl.split("/a/")[1]
			url = "http://localhost/php/album.php?album="+albumid
			request = urllib2.Request(url, headers={})
			contents = urllib2.urlopen(request).read()
			for x in contents.split("\n"):
				if x is not "":
					sql = "INSERT INTO buns (url) VALUE (%s)"
					try:
						cursor.execute(sql, (x, ))
						db.commit()
					except:
						print sys.exc_info()
						db.rollback()
						print "[DB ERROR] Can't add bun from album"
		except urllib2.URLError as e:
			print e
			print url
			return "Error opening URL"
	else:
		url = message
		sql = "INSERT INTO buns (url) VALUE (%s)"
		try:
			cursor.execute(sql, (url, ))
			db.commit()
		except:
			print sys.exc_info()[0]
			db.rollback()
			print "[DB ERROR] Can't add bun"


def getcat():
	sql = "SELECT url,id FROM cats WHERE used = 0 ORDER BY id ASC"
	try:
		cursor.execute(sql, ())
		data = cursor.fetchone()
		incbun(int(data[1]))
		return data[0]+" CoolCat"
	except:
		print sys.exc_info()[0]
		db.rollback()
		print "[DB ERROR] Can't get cat"
		return "Cat dispenser empty. Please ask your cat attendant to pour in more cat."


def inccat(id):
	sql = "UPDATE cats SET used = 1 WHERE used = 0 AND id = %s"
	try:
		cursor.execute(sql, (id, ))
		db.commit()
	except:
		print sys.exc_info()[0]
		db.rollback()
		print "[DB ERROR] Can't update cat"


def addcat(message):
	if message[0] == "-":
		try:
			albumurl = message.split(" ")[1]
			albumid = albumurl.split("/a/")[1]
			url = "http://localhost/php/album.php?album="+albumid
			request = urllib2.Request(url, headers={})
			contents = urllib2.urlopen(request).read()
			for x in contents.split("\n"):
				if x is not "":
					sql = "INSERT INTO cats (url) VALUE (%s)"
					try:
						cursor.execute(sql, (x, ))
						db.commit()
					except:
						print sys.exc_info()
						db.rollback()
						print "[DB ERROR] Can't add cat from album"
		except urllib2.URLError as e:
			print e
			print url
			return "Error opening URL"
	else:
		url = message
		sql = "INSERT INTO cats (url) VALUE (%s)"
		try:
			cursor.execute(sql, (url, ))
			db.commit()
		except:
			print sys.exc_info()[0]
			db.rollback()
			print "[DB ERROR] Can't add cat"
