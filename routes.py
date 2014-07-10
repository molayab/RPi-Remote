#!/usr/bin/python

from flask import Flask 
from flask import send_from_directory
from flask import render_template as render
from flask import jsonify as json_response

from subprocess import PIPE, Popen
from ConfigParser import SafeConfigParser

import os
import json

# CONFIGURACION INICIAL 
config = SafeConfigParser()
config.read('config/config.ini')

HOST = config.get('default', 'host')
PORT = config.getint('default', 'port')
DEBUG = config.getboolean('default', 'debug')
RELOADER = config.getboolean('default', 'use_reloader')

#########################

app = Flask(__name__)
app.debug = DEBUG

## Drives ##
drives = {}

with open("config/drives.json") as file:
	drives = json.load(file)

def get_files(path):
	def get_kind(dir, filename):
		if filename.find(".") == 0:
			if os.path.isdir("%s/%s" % (dir, filename)):
				return "inode"
			return "hidden"
		elif os.path.isdir("%s/%s" % (dir, filename)):
			return "inode"
		elif filename.find(".") > 0:
			return filename.split(".")[-1]
		else:
			return "unknown"

	files = {}

	if not path:
		for disk, path in drives.iteritems():
			files[disk] = {"path": disk, "kind": "drive"}
	else:
		disk = path.split("/")[0];
		realpath = drives[disk] + path[len(disk):]

		if os.path.isdir(realpath):
			for file in os.listdir(realpath):
				files[file] = {
					"path": "%s/%s" % (path, file), 
					"kind": get_kind(realpath, file)
				}
		elif os.path.isfile(realpath):
			try:
				filename = realpath.split("/")[-1]

				directory = realpath[:len(filename) * -1]

				return (False, send_from_directory(
                			directory=directory,
                			filename=filename,
                			as_attachment=False))
			except:
				pass

	return True, files


def system_monitor():
	import psutil as core

	def get_cpu_temperature():
		try:
			process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)

			output, _error = process.communicate()
			return float(output[output.index('=') + 1:output.rindex("'")])
		except:
			return -1

	ret = {}

	ret['cpu'] = {
		"percent": core.cpu_percent(),
		"times": {
			"user": core.cpu_times().user,
			"system": core.cpu_times().system,
			"idle": core.cpu_times().idle
		},
		"temp": get_cpu_temperature()
	}

	ret['memory'] = {
		"virtual": {
			"total": core.virtual_memory().total,
			"available": core.virtual_memory().available,
			"used": core.virtual_memory().used,
			"free": core.virtual_memory().free,
		},

		"swap": {
			"total": core.swap_memory().total,
			"used": core.swap_memory().used,
			"free": core.swap_memory().free
		}
	}

	disks = {}

	for disk in core.disk_partitions():
		usage = core.disk_usage(disk.mountpoint)

		disks[disk.device] = {
			"mount": disk.mountpoint, 
			"type": disk.fstype,
			"size": {
				"total": usage.total,
				"used": usage.used,
				"free": usage.free
			}
		}

	ret["disks"] = disks

	processes = {}
	try:
		for process in core.pids():
			p = core.Process(process)

			processes[p.name()] = {
				"status": p.status(),
				"exec": p.cmdline(),
				"user": p.username(),
				"cpu": p.cpu_percent(),
				"memory": p.memory_percent(),
				"threads": p.num_threads(),
			}
	except:
		pass

	ret['processes'] = processes

	return ret


@app.route("/")
@app.route("/index")
def index():
	return render("index.html", status=system_monitor())

@app.route("/drive")
@app.route("/drive/<path:path>")
def drive(path = None):
	is_list, files = get_files(path)

	if is_list:
		return render("drive.html", files = files, path=path)
	else:
		return files

@app.route("/api/drive")
@app.route("/api/drive/<path:path>")
def api_drive(path = None):
	is_list, files = get_files(path)

	return json_response(files)

@app.route("/dashboard")
def dashboard():
	return render("dashboard.html", status=system_monitor())

@app.route("/api/icon/<ext>")
def icon(ext = "unknown"):
	icon_path = "static/img/icons"
	icon_file = "z File %s.png" % ext.upper()

	if os.path.isfile("%s/%s" % (icon_path, icon_file)):
		return send_from_directory(icon_path, icon_file)
	else:
		return send_from_directory(icon_path, "z File UNKNOWN.png")

@app.route("/api/core")
@app.route("/api/core/<tag>")
def core(tag = None):
	info = system_monitor()

	if not tag:
		return json_response(info)
	try:
		return json_response(info[str(tag)])
	except:
		return json_response({"error": 404})

@app.context_processor
def utility_processor():
	def sizeof_fmt(num, fmt = True):
		for x in ['bytes','KB','MB','GB','TB']:
			if num < 1024.0:
				return "%3.1f %s" % (num, x) if fmt else "%3.1f" % num
			num /= 1024.0
	return dict(sizeof_fmt=sizeof_fmt)


if __name__ == "__main__":
	app.run(host=HOST, port=PORT, use_reloader=RELOADER)

