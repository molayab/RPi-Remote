#!/usr/bin/python

import sqlite3 as lite
from subprocess import PIPE, Popen
import psutil as core
import ntplib
from time import ctime



""""

SQL TEMPERATURA

BEGIN;


-- CREATE TABLE "cpu" ------------------------------------------
CREATE TABLE "cpu"(
	"id" DateTime NOT NULL PRIMARY KEY,
	"percent" Integer NOT NULL,
	"temperature" Integer NOT NULL );

-- Create index index_cpu_percent
CREATE INDEX "index_cpu_percent" ON "cpu"( "percent" );





-- Create index index_temperature
CREATE INDEX "index_temperature" ON "cpu"( "temperature" );
-- -------------------------------------------------------------;

COMMIT;
"""

def temperature(tries = 0):
	try:
		c = ntplib.NTPClient()
		response = c.request('pool.ntp.org')
		time = ctime(response.tx_time)

		db = lite.connect("kernel.db")
		cursor = db.cursor()

		process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)

		output, _error = process.communicate()

		temp = float(output[output.index('=') + 1:output.rindex("'")])
		load = core.cpu_percent()

		cursor.execute('''INSERT INTO cpu(id,percent,temperature) VALUES (?,?,?);''', (time, int(load), int(temp)))

		db.commit()
	except Exception, e:
		if tries < 10:
			temperature(tries=tries+1);
		else:
			print e

temperature()