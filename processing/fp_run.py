#!/usr/bin/env python2
# vim: sts=4 ts=4 sw=4 noet:

from __future__ import print_function
import sys
import os
import argparse

import numpy as np

import pretty_logger
logger = pretty_logger.get_logger()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description='Program Action: Run image processing',
			epilog='''\
Control debug level with DEBUG evinronment environment variable.
  Default: no debugging
  DEBUG=1: print debugging information
  DEBUG=2: print lots of debugging information

  QUIET=1: Suppress most output (supersedes DEBUG)

  PICS=1:  Save intermediate images (slow)
''')
	parser.add_argument('-f', '--filename', type=str,
			default='./samples/x_0_y_0.jpg',
			#default='./samples/x_0_y_1.27.jpg',
			help='image to process')
	parser.add_argument('-c', '--camera', type=str,
			#default='lumia_1020',
			default='iphone7-front',
			help='phone type; must be in phones/')
	parser.add_argument('-m', '--method', type=str,
			default='opencv_fft',
			help='image processing method; must be in processors/')
	parser.add_argument('-r', '--room', type=str,
			#default='test_rig',
			default='demo_floor',
			help='room the image was taken in; must be in rooms/')

	args = parser.parse_args()

	#parser.print_help()

	os.environ["DEBUG"]="1"
	#os.environ["PICS"]="1"

	np.set_printoptions(suppress=True)


	try:
		#from phones import args.camera.split('-')[0] as phone
		phone = __import__('phones.' + args.camera.split('-')[0], fromlist=[1,])
	except ImportError:
		logger.error("Unknown phone: {}".format(args.camera.split('-')[0]))
		raise
	try:
		camera = getattr(phone, args.camera.split('-')[1])
	except IndexError:
		# A camera was not specified, use the default (elem 0) for this phone
		camera = phone.cameras[0]
	except AttributeError:
		# Found the phone, but not the specified camera
		logger.error("Unknown phone / camera combination")
		raise

	try:
		imag_proc = __import__('processors.' + args.method, fromlist=[1,]).imag_proc
	except ImportError:
		logger.error('Unknown image processing backend.')
		raise

	from fingerprint import fingerprint

	try:
		room = __import__('rooms.' + args.room, fromlist=[1,])
	except ImportError:
		logger.error('Unknown room')
		raise

	try:
		rx_location = fingerprint(
				args.filename,
				camera, room,
				imag_proc
				)
		logger.info('rx_location = {}'.format(rx_location))
	except Exception as e:
		logger.warn('Exception: {}'.format(e))
		raise

