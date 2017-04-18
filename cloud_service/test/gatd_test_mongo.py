#!/usr/bin/env python

import sys
import time
import json
import urllib2
import random
import socket
import argparse

HOST = '140.118.170.52'
PROFILE_ID = 'mongo.php'
POST_URL = 'http://' + HOST + '/' + PROFILE_ID

def post_pkt(idx, phone_ip, user):
	#p = random.choice(data)
	p = data[idx]
	pkt = {
			'rx_location': p['rx_location'],
			'rx_rotation': p['rx_rotation'],
			'location_error': p['location_error'],
			'image_name': p['image_name'],
			'phone_ip' : phone_ip,
			'user': user,
			}

	req = urllib2.Request(POST_URL)
	req.add_header('Content-Type', 'application/json')

	response = urllib2.urlopen(req, json.dumps(pkt))
	print("Posted pkt #{}".format(idx))

data = [
{u'_receiver': u'http_post', u'_processor_count': 0, u'profile_id': u'WEgwAGyc9N', u'image_name': u'2014-09-07--21-56-18-04', u'rx_rotation': [[0.014336268087278349, 1.021694671550933, 0.0804287416674231], [-0.7853248943169617, 0.044185912924521856, -0.5778365927334801], [-0.5701501006094175, -0.06855363180211634, 0.8122633033373631]], u'rx_location': [12.89953801157171, -98.55280661446464, 127.78643457463806], u'location_error': 0.9737737053724231, u'time': 1410141807039, u'_id': u'540d0e6f7f82e72e099f23c6', u'port': 50473, u'address': u'281471087271422'},
{u'_receiver': u'http_post', u'_processor_count': 0, u'profile_id': u'WEgwAGyc9N', u'image_name': u'2014-09-07--21-56-01-00', u'rx_rotation': [[-0.0456745453247575, -0.9937648779371678, 0.04103443419847221], [0.8763630535911789, -0.013842466402105926, 0.4842408528088045], [-0.45328688836223213, 0.028263638339037816, 0.8733387477481256]], u'rx_location': [8.991988333114621, 86.55352645581408, 127.69217094040292], u'location_error': 1.404359065164499, u'time': 1410141790371, u'_id': u'540d0e5e7f82e72e099f21cd', u'port': 50471, u'address': u'281471087271422'},
]

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Unduly complex test script.')
	parser.add_argument('--count', type=int, default=10)
	parser.add_argument('--delay', type=float, default=.5)
	parser.add_argument('--index', type=int, default=-1)
	parser.add_argument('--ip', type=str, default='')
	parser.add_argument('--user', type=str, default='')

	args = parser.parse_args()

	if args.index == -1:
		args.index = random.choice(range(len(data)-args.count))
	if args.ip == '':
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect((HOST,PORT))
		args.ip = s.getsockname()[0]
		s.close()
	if args.user == '':
		args.user = socket.gethostname().split('.')[0]

	for i in range(args.count):
		post_pkt(args.index + i, args.ip, args.user)
		time.sleep(args.delay)
