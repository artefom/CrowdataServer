from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, world!'

if __name__ == '__main__':

	f = open('server.cfg')
	lines = [line for line in f]
	serverType = lines[0]
	ip, port = lines[1].strip().split(':')

	app.run(ip,int(port))
