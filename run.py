import sensor as s
import MySQLdb as mdb
from config import *

con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DATABASE)

with con:
	cursor = con.cursor()
	query = "SELECT * FROM sensors WHERE enabled = 1"
	cursor.execute(query)
	result = cursor.fetchall()
	sensors = []
	for sensor in result:
		x = s.Temperature(sensor[2])
		sensors.append(x)
	for sensor in sensors:
		sensor.start()
