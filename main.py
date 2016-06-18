from flask import Flask
import logging
from multiprocessing import Process
import json
import random

#import crowdata packages and modules
import utests
import datamodel
import glob
import apiwrappers
import apiwrappers.responses

open('server.log', 'w').close()
logging.basicConfig(filename='server.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.error('And this, too')

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

	resp = json.dumps(resp,indent = 4)
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
	glob.SetGlobalParameters()

	sampleArr = []
	for i in range(100):
		ri = apiwrappers.responses.base(apiwrappers.SOCIALMEDIAS.instagram, 
				(random.uniform(55.56747507540021,55.92150795277898),
				random.uniform(37.371368408203125,37.863006591796875)),
				i)
		sampleArr.append(ri)

	print('adding raw info List')
	print('mat = ',glob.mat)
	glob.mat.addRawInfoList(sampleArr)

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

	# server config
	server_cfg_path = "server.cfg"
	server_cfg = {'ip' : 'localhost','port' : 50000}
	
	# debug condig, has priority over server config and overwrites it
	debug_cfg_path = "debug.cfg"
	debug_cfg = dict()

	try:
		with open(server_cfg_path) as data_file:
			server_cfg = json.load(data_file)
	except:
		logging.error('Unable to load'+server_cfg_path)

	try:
		with open(debug_cfg_path) as data_file:
			debug_cfg = json.load(data_file)
	except:
		logging.error('Unable to load'+debug_cfg_path)


	#overwrite config from server.cfg with debug.cfg

	cfg = glob.dict_merge_overwrite(server_cfg,debug_cfg)

	if cfg.get("debug",0):
		pass
	else:
		pass

	# #Load server config (server\debug mode, ip, port)
	# #Used to determine, weather current server is in production, or debug
	# #You should add server.cfg to .gitignore
	# f = open('server.cfg')
	# lines = [line for line in f]
	# serverType = lines[0]

	# #if first line of server.cfg is 'server', than server is in production
	# if (serverType.strip() == 'server'):
	# 	isServer = True

	# #Execute unit tests, if server is not in production
	# if (not isServer):
	# 	utests.startTests()

	# #Gather ip and port from server.cfg
	# ip, port = lines[1].strip().split(':')

	# #Initialize data sctructures in debug mode
	# InitializeServer_Debug()

	# print('Server executed at ',ip,':',port,sep='')

	# startApp(ip,port)