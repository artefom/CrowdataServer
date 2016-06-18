from flask import Flask
import logging
import utests
from multiprocessing import Process
import mainloop
import dataCells
import json
from glob import *
import glob

open('ignored/server.log', 'w').close()
logging.basicConfig(filename='ignored/server.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/circles/<lat1>&<lng1>&<lat2>&<lng2>')
def circlesRequest(lat1,lng1,lat2,lng2):

	circles = glob.getCircles(float(lat1),float(lng1),float(lat2),float(lng2))
	resp = dict()
	resp['lng'] = [i[0] for i in circles]
	resp['lat'] = [i[1] for i in circles]
	resp['size'] = [i[2] for i in circles]

	resp = json.dumps(resp)
	return resp

""" When this code is in production, this variable should be True
"""
isServer = False

""" Executes server at ip and port
"""
def startApp(ip,port):
	app.run(ip,int(port),debug=True,use_reloader=False)


""" Debug mode initialization
	It's supposed to initialize dataCell with test Values,
	or load them from saved file etc.
"""
def InitializeServer_Debug():
	logging.info('Server Debug initialization')
	SetGlobalParameters()
	utests.addRandomData()

""" Production mode initialization
	It's supposed to load previously saved data from disk and
	put it into dataCell
"""
def InitializeServer():
	logging.info('Server initialization')
	pass

""" It's called when server is about to shut down
"""
def FinilizeServer():
	logging.info("server finalization")
	pass

""" Loop, reading command line or gathering information from web
	when this method finishes, server shuts down
"""
def MainLoop():
	logging.info("Main loop entered")
	logging.info("Main loop finalized")

if __name__ == '__main__':

	#Load server config (server\debug mode, ip, port)
	#Used to determine, weather current server is in production, or debug
	#You should add server.cfg to .gitignore
	f = open('server.cfg')
	lines = [line for line in f]
	serverType = lines[0]

	#if first line of server.cfg is 'server', than server is in production
	if (serverType.strip() == 'server'):
		isServer = True

	#Execute unit tests, if server is not in production
	if (not isServer):
		utests.startTests()

	#Gather ip and port from server.cfg
	ip, port = lines[1].strip().split(':')

	#Initialize data sctructures in debug mode
	InitializeServer_Debug()

	print('Server executed at ',ip,':',port,sep='')

	startApp(ip,port)