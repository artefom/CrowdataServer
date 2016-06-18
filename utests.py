import dataCells
import os
from apiBase import *
import random
import glob
import json

def addRandomData():

	sampleArr = []
	for i in range(100):
		ri = RawInfo(SOCIALMEDIAS.instagram, 
				(random.uniform(55.56747507540021,55.92150795277898),
				random.uniform(37.371368408203125,37.863006591796875)),
				i)
		sampleArr.append(ri)

	print('adding raw info List')
	print('mat = ',glob.mat)
	glob.mat.addRawInfoList(sampleArr)

def startTests():
	pass
	#glob.SetGlobalParameters()


	# print("Test started")
	# addRandomData()
	# print("Getting circles")
	# circles = glob.getCircles(55.92150795277898,37.371368408203125,55.56747507540021,37.863006591796875)
	# print("circles",circles)
	# resp = dict()
	# resp['lng'] = [i[0] for i in circles]
	# resp['lat'] = [i[1] for i in circles]
	# resp['size'] = [i[2] for i in circles]
	# resp = json.dumps(resp)
	# print("Response:\n",resp)

if __name__ == '__main__':
	os.system("python main.py")