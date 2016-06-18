from flask import Flask
import logging
import utests

open('ignored/server.log', 'w').close()
logging.basicConfig(filename='ignored/server.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, world!'

isServer = False

if __name__ == '__main__':

	f = open('server.cfg')
	lines = [line for line in f]
	serverType = lines[0]

	if (serverType.strip() == 'server'):
		isServer = True

	if (not isServer):
		utests.startTests()

	ip, port = lines[1].strip().split(':')

	if (isServer):
		app.run(ip,int(port))
