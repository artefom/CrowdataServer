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
import pickle
from flask import Flask, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper

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

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/circles/<lat1>&<lng1>&<lat2>&<lng2>')
@crossdomain(origin="*")
def circlesRequest(lat1,lng1,lat2,lng2):

	logging.debug('processing request for '+str(lat1)+','+str(lng1)+','+str(lat2)+','+str(lng2) )

	try:


		circles, locations, cell_size = glob.getCircles(float(lat1),float(lng1),float(lat2),float(lng2))

		locations_data = []

		for i in locations:
			try:
				locations_data.append( i.data )
			except:
				pass
		
		#circles = glob.getCircles(float(lat1),float(lng1),float(lat2),float(lng2))
		sizes = np.array([i[2] for i in circles])
		count = sizes
		sizes = sizes-sizes.min()
		sizes = sizes/sizes.max()
		sizes2 = np.sqrt(sizes)*cell_size*1.3
		sizes = np.sqrt(sizes*3)
		sizes = sizes/sizes.max()
		sizes = 2+sizes*8

		resp = dict()
		resp['lat'] = [i[0] for i in circles]
		resp['lng'] = [i[1] for i in circles]
		resp['size'] = sizes.tolist()
		resp['size2'] = sizes2.tolist()
		resp['count'] = count.tolist()
		resp['events'] = locations_data

		resp = json.dumps(resp,indent = 4,ensure_ascii=False)

		return resp
	except:
		pass

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

	# sampleArr = []
	# for i in range(500):
	# 	ri = apiwrappers.responses.base(apiwrappers.SOCIALMEDIAS.instagram, 
	# 			(random.uniform(55.56747507540021,55.92150795277898),
	# 			random.uniform(37.371368408203125,37.863006591796875)),
	# 			i)
	# 	sampleArr.append(ri)
	#   glob.mat.addRawInfoList(fbdata)

	# with open('fb_data.dat','rb') as file_data:
	# 	raw_data = pickle.load(file_data)
	
	# fbdata = apiwrappers.responses.facebook.list_from_raw_data(raw_data)

	# glob.mat.addRawInfoList(fbdata)

	fb_events = apiwrappers.responses.facebook_event.list_from_file('fb_events_data.dat')
	glob.mat.addRawInfoList(fb_events)

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
