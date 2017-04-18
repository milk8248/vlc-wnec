#!/usr/bin/env python
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys, os
import argparse

import numpy
import numpy.ma
import scipy
import scipy.misc
import scipy.ndimage
import scipy.signal
import scipy.cluster
import matplotlib
import matplotlib.mlab
import pylab
import json

import pymongo
from pymongo import MongoClient

from operator import itemgetter,attrgetter

import pretty_logger
logger = pretty_logger.get_logger()

def sort_by_fingerprint(d):
    '''a helper function for sorting'''
    return d['fingerprint']

@logger.op("Fingerprint")
def fingerprint(now_lights, camera, room, imag_proc):

	try:
		now_lights_frequency_array=[]
		for light in now_lights:
			now_lights_frequency_array=numpy.append(now_lights_frequency_array,light['frequency'])

		client = MongoClient('140.118.170.52', 27017)
		db = client.vlc_demo
		collect = db.fingerprint
		fp_data = collect.find({'lights_info.frequency':{'$all':numpy.array(now_lights_frequency_array).tolist()}})
		fp_data = list(fp_data)


		sign=0
		for i in fp_data:
			if sign == 0:
				minfp = i
				sign = 1
			
			del i['_id']
			# fp_data=json.dumps(i, sort_keys=True)
			num_lights=0
			c = 0
			
			for light in i['lights_info']:
				for now_light in now_lights:
					if now_light['frequency'] == light['frequency']:
						a=numpy.sqrt(light['image_location'][0]**2+light['image_location'][1]**2)
						b=numpy.sqrt(now_light['image_location'][0]**2+now_light['image_location'][1]**2)
						# c+=numpy.abs(a-b)
						c+=numpy.abs((a-b)**2)
						num_lights+=1
			c=numpy.sqrt(c)
			i['fingerprint']=c
			if i['fingerprint']<minfp['fingerprint'] :
				minfp=i
		# assert minfp['fingerprint'] < 100, "NONONONONONO"
		
		fp_data=sorted(fp_data, key=sort_by_fingerprint)

		fp_no_dup=[]
		for i in xrange(len(fp_data)):
			p=False
			if i==0:
				fp_no_dup.append(fp_data[i])
			for j in xrange(len(fp_no_dup)):
				if fp_data[i]['origin_location'] != fp_no_dup[j]['origin_location']:
					p=True
				else:
					p=False
					break
			if p==True:
				fp_no_dup.append(fp_data[i])
		# for i in fp_data:
		#  	print(i['origin_location'])
		#  	print(i['fingerprint'])
		
		#get top 4 data
		fp_data_top4 = fp_no_dup[:4]
		fingerprint = []
		origin_location = []
		for j in fp_data_top4:
			j['origin_location']=numpy.array(j['origin_location'])*10
			logger.debug("Fingerprint result top: {} - {} - {}".format(j['image_name'],j['fingerprint'],j['origin_location']))
			fingerprint = numpy.append(fingerprint,j['fingerprint'])
		# print(fingerprint)
		if fp_data_top4[0]['fingerprint'] <=40:
			rx_location_fp=fp_data_top4[0]['origin_location']
		else:
			fingerprint = (1/fingerprint**2)/sum(1/fingerprint**2)
			rx_location_fp=0
			for i in xrange(len(fingerprint)):
				rx_location_fp=rx_location_fp+fp_data_top4[i]['origin_location']*fingerprint[i]	

		# >70
		# fingerprint = (1/fingerprint**2)/sum(1/fingerprint**2)
		# rx_location_fp=0
		# if fingerprint[0]>=70:
		# 	rx_location_fp=fp_data_top4[0]['origin_location']
		# else:
		# 	for i in xrange(len(fingerprint)):
		# 		rx_location_fp=rx_location_fp+fp_data_top4[i]['origin_location']*fingerprint[i]	


		logger.debug("Fingerprint result location : {}".format(rx_location_fp))

		# for i in fp_data:
		# 	print(minfp)
		# 	if i['fingerprint'] == minfp:
		# 		print(i)


		# 	temp=i['fingerprint']
		# 	if i['fingerprint']:
		# 		minfp = i['fingerprint']
		# 		i['min']=True
		
		# 	print(tempfp['image_name'])
		# 	# for j in range(len(i['lights_info'])):
			# 	print(i['lights_info'][j]['frequency'])
			# 	for k in range(len(actual_frequencies)):
			# 		if actual_frequencies[k] == i['lights_info'][j]['frequency']:
			# 			i['']
			# 		print(i['image_name'])

		#fp_data = collect.find()

	except pymongo.errors.ConnectionFailure:
		logger.info('No MongoDB Found')

	return (rx_location_fp)
