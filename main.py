from flask import Flask
import logging
from multiprocessing import Process
import multiprocessing
import json
import random
import datetime
import weakref
import time
import _thread
from flask import request
import os
import signal
import numpy as np

#import crowdata packages and modules
import utests
import datamodel
import glob
import apiwrappers
import apiwrappers.responses

open('server.log', 'w').close()
logging.basicConfig(filename='server.log',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.error('And this, too')

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/circles/<lat1>&<lng1>&<lat2>&<lng2>')
def circlesRequest(lat1,lng1,lat2,lng2):

	logging.debug('processing request for '+str(lat1)+','+str(lng1)+','+str(lat2)+','+str(lng2) )

	circles = glob.getCircles(float(lat1),float(lng1),float(lat2),float(lng2))
	sizes = np.array([i[2] for i in circles])
	sizes = sizes-sizes.min()
	sizes = sizes/sizes.max()
	sizes = np.sqrt(sizes*3)
	sizes = sizes/sizes.max()
	sizes = 2+sizes*8

	resp = dict()
	resp['lat'] = [i[0] for i in circles]
	resp['lng'] = [i[1] for i in circles]
	resp['size'] = sizes.tolist()

	resp = json.dumps(resp,indent = 4)

	return resp


""" When this code is in production, this variable should be True
"""
isServer = False

""" Executes server at ip and port
"""
def startApp(ip,port):
	logging.info('startApp')
	#print("Listening " + ip+":"+ port ) 
	app.run(ip,int(port),debug=True,use_reloader=False)


""" Debug mode initialization
	It's supposed to initialize dataCell with test Values,
	or load them from saved file etc.
"""
def InitializeServer_Debug():
	logging.info('Server Debug initialization')
	glob.SetGlobalParameters()

	sampleArr = []
	for i in range(500):
		ri = apiwrappers.responses.base(apiwrappers.SOCIALMEDIAS.instagram, 
				(random.uniform(55.56747507540021,55.92150795277898),
				random.uniform(37.371368408203125,37.863006591796875)),
				i)
		sampleArr.append(ri)

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


""" Web crawler, crawls through web, gathering information once a hour o 30 mins
	Should be infinite loop.
"""
class webcrawler(multiprocessing.Process):

	def __init__(self, ):
		multiprocessing.Process.__init__(self)
		self.exit = multiprocessing.Event()

	def run(self):
		while not self.exit.is_set():
			time.sleep(1)
			logging.info( "Crawler crawls. Time: "+str(datetime.datetime.now()) )
		logging.info("Crawler exits")
		app.stop()

	def shutdown(self):
		self.exit.set()


""" Loop, reading command line or gathering information from web
	when this method finishes, server shuts down
"""
def process_stdin():
	logging.info("Main loop entered")
	
	print("waiting for standard input... ('exit' to exit)")
	
	while True:
		command = input()
		logging.info("console command recieved: "+command)
		if (command == "exit"):
			break

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
		InitializeServer_Debug()
		utests.startTests()
	else:
		InitializeServer_Debug()

	_thread.start_new_thread( startApp, (cfg['ip'],cfg['port']) )

	process_stdin()
	

	#startApp(cfg['ip'],cfg['port'])
