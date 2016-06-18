from flask import Flask


@app.route('/')
def hello_world():
	return 'Hello, world!'

if __name__ == '__main__':
	app.run('0.0.0.0',80)
