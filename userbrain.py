#!/usr/bin/env python
# encoding: utf-8
"""
userbrain.py

Created by Michael Sobczak on 2012-07-25.
Copyright (c) 2012 Michael Sobczak. All rights reserved.
"""

import Queue
from threading import Thread, Event
from socket import *
import json
import time

# local imports
from utils import dict_string

HOST = '127.0.0.1'
PORT = 13854
ADDR = (HOST, PORT)
APP_NAME = 'Python'
USER_NAME = 'Anonymous'
headset_conf_dict = {'enableRawOutput':False, 'format':'Json'}
HEADSET_JSON_SEPARATOR = '\r'


brain_parameters = (lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, highGamma, delta, theta, poorSignalLevel, meditation, attention) = ('lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma', 'delta', 'theta', 'poorSignalLevel', 'meditation', 'attention')
parameter_categories = (eSense, eegPower) = ('eSense', 'eegPower')

NULL_DATA = {poorSignalLevel:200}

def debug(msg):
	print msg

def _extract_tuple(data_dict):
	return (
		data_dict[eegPower][lowAlpha],
		data_dict[eegPower][highAlpha],
		data_dict[eegPower][lowBeta],
		data_dict[eegPower][highBeta],
		data_dict[eegPower][lowGamma],
		data_dict[eegPower][highGamma],
		data_dict[eegPower][delta],
		data_dict[eegPower][theta],
		data_dict[poorSignalLevel],
		data_dict[eSense][meditation],
		data_dict[eSense][attention])
	
def _datastream(check_continue_func, host=HOST, port=PORT):
	cs = socket(AF_INET, SOCK_STREAM)
	cs.connect((host, port))
	cs.send(json.dumps(headset_conf_dict))
	data = None
	while check_continue_func():
		temp_json = ''
		cur_char = cs.recv(1)
		while cur_char != '\r':
			temp_json += cur_char
			cur_char = cs.recv(1)
		data = json.loads(temp_json)
		yield data
	cs.close()
	yield data
	
	
def _processDataStream(output_queue, shutdown_flag, connected_flag, host, port):
	# make the datastream generator
	ds = _datastream(lambda: not shutdown_flag.isSet(), host, port)
	# make a json processor
	json_processor = lambda: ds.next()
	# get connected properly and start receiving real data before moving on
	#debug('Attempting to connect to headset...')
	while not connected_flag.isSet():
		raw_data = json_processor()
		if not raw_data == NULL_DATA:
			# getting real data now
			connected_flag.set()
	# should now be getting real data

	for d in ds:
		raw_data = json_processor()
		if eegPower in raw_data and eSense in raw_data:
			# full data set, extract and pump it
			flat_data = dict(zip(brain_parameters, _extract_tuple(raw_data)))
			output_queue.put(flat_data)

	connected_flag.clear()
	
	
class Brain(object):
	
	def __init__(self, host=HOST, port=PORT, appName=APP_NAME, userName=USER_NAME):
		self.queue = Queue.Queue()
		self.host = host
		self.port = port
		self.app_name = appName
		self.user_name = userName
		self.shutdown_stream = Event()
		self.is_connected_flag = Event()
		self.producer_thread = Thread(target=_processDataStream, args=(self.queue, self.shutdown_stream, self.is_connected_flag, host, port))
		self.freshest_data = None
		self.producer_thread.start()

	def isConnected(self):
		return self.is_connected_flag.isSet()
		
		
	def getProperty(self, propertyName):
		if not self.queue.empty():
			self.freshest_data = self.queue.get(False)
		return self.freshest_data[propertyName] if propertyName in self.freshest_data else None
		
	def __del__(self):
		print 'Inside delete method of brain: %s' % str(self)
		self.shutdown_stream.set()
		self.producer_thread.join()	
		
	def __str__(self):
		template = 'Brain:\n\thost: %s\tport: %d\n\tappName: %s\tuserName: %s'
		return template % (str(self.host), self.port, self.app_name, self.user_name)
		
	
		

def testBrain():
	import code
	my_brain = Brain()
	while not my_brain.isConnected():
		print 'brain not yet connected, trying again in 5 seconds'
		time.sleep(5)
	print 'brain now connected presumably, lets get some data'
	print 'lowAlpha: %d\tattention: %f' % (my_brain.getProperty(lowAlpha), my_brain.getProperty(attention))
	print 'sleep for 3 seconds then check again'
	time.sleep(3)
	print 'new data:'
	print 'lowAlpha: %d\tattention: %f' % (my_brain.getProperty(lowAlpha), my_brain.getProperty(attention))
	
if __name__ == '__main__':
	testBrain()