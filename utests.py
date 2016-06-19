import os
import random
import json

import glob
import apiwrappers
import apiwrappers.responses
import datamodel

"""
	This executed before server start in debug mode
"""
def startTests():

	print("Tests executed")

	# global mat

	# lat1_old = 55.92150795277898
	# lng1_old = 37.371368408203125
	# lat2_old = 55.56747507540021
	# lng2_old = 37.863006591796875

	# lat1 = lat1_old*0.51+lat2_old*0.49
	# lat2 = lat1_old*0.49+lat2_old*0.51

	# lng1 = lng1_old*0.51+lng2_old*0.49
	# lng2 = lng1_old*0.49+lng2_old*0.51

	# circles = glob.getCircles(float(lat1),float(lng1),float(lat2),float(lng2))
	# resp = dict()
	# resp['lat'] = [i[0] for i in circles]
	# resp['lng'] = [i[1] for i in circles]
	# resp['size'] = [i[2] for i in circles]

	# resp = json.dumps(resp,indent = 4)

	# print(resp)