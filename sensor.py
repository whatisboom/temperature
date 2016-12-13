from threading import Thread
import MySQLdb as mdb
import time
from config import *


class Temperature(Thread):

	def __init__(self, hwid, fnpattern=None):
		if fnpattern is None:
			fnpattern = '/sys/bus/w1/devices/{0}/w1_slave'

		self.hwid = hwid
		self.filename = fnpattern.format(hwid)
		self.lasttemp = 0
		Thread.__init__(self)
	def run(self):
		while True:
			try:
				f = open(self.filename)
			except IOError as e:
				print "Error: Sensor does not exist: " + self.filename
				return
			lines = f.read()
			f.close
			data = lines.split("\n")
			crc = data[0].split(" ")[len(data[0].split(" "))-1]
			temp = float(data[1].split(" ")[9].split("=")[1])/1000
			if crc == "YES" and temp != self.lasttemp:
				self.lasttemp = temp
				con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DATABASE)
				with con:
					cursor = con.cursor()
					query = "INSERT INTO data (sensor, temp) VALUES ('{0}', {1})" .format(self.hwid, self.lasttemp)
					cursor.execute(query)
#					print "Saving temperature: {1}, from sensor: {0}".format(self.hwid, self.lasttemp)
				time.sleep(600)
