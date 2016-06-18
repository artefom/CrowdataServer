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

isServer = False

def startApp(ip,port):
	app.run(ip,int(port),debug=True)

""" Datamatrix - main data container
"""

if __name__ == '__main__':

	SetGlobalParameters()
	utests.addRandomData()

	f = open('server.cfg')
	lines = [line for line in f]
	serverType = lines[0]

	if (serverType.strip() == 'server'):
		isServer = True

	if (not isServer):
		utests.startTests()

	ip, port = lines[1].strip().split(':')

	print('ip',ip,'port',port)
	startApp(ip,port)
	#p = Process(target=startApp,args=(ip,port))
	#p.start()
	#mainloop.mainLoop()
	#p.terminate()
	#p.join()

	#app.run(ip,int(port))
