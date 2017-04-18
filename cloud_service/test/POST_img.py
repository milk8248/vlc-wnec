#!/usr/bin/env python

import requests
import socket
import sys
import os
import numpy

if len(sys.argv) < 2:
	print('One arg (file) req\'d')
	sys.exit(1)

fname = sys.argv[1]

try:
	host = sys.argv[2]
except IndexError:
	host = 'localhost'

try:
	user = sys.argv[3]
except IndexError:
	user = socket.gethostname().split('.')[0]

r = requests.post('http://'+host+':5102/offline/'+os.path.basename(fname),
		headers={
			'content-type': 'image/jpeg',
			'X-luxapose-phone-type': 'iphone7',
			'X-luxapose-camera': 'front',
			'X-luxapose-ble-loc-hints': 'atrium',
			'X-luxapose-user': user,
			'x-luxapose-device-uuid': 'tCdlp0tC188kB1ppE8MCaMmmwd8=',
			'x-luxapose-origin-location' : '-5,-6,0'
			},
		data=open(fname, 'rb'))
print(r.status_code)

