#!/usr/bin/env python
# encoding: utf-8
"""
userbrain.py

Created by Michael Sobczak on 2012-07-25.
Copyright (c) 2012 Michael Sobczak. All rights reserved.

This module is to be used for interacting with brainwave headsets that communicate using the
ThinkGearConnector server. Contained within this module are classes that allow for different
use cases of the MindWave technology. Users of this module who want to dynamically grab the
most recent state of the brain received from the headset should focus on the Brain class while
those who want to get a generator and explicitly process each incoming message should stick to
the BrainStream class. More can be found on these classes in their docs.
"""

# external imports
# threading stuff
import Queue
from threading import Thread, Event
# networking stuff
from socket import *
# misc.
import json
import time


# these are used as default parameters for the classes in this module. They come from the default
# factory settings on the MindWave brand of headsets.
# TODO: move these into a configuration file
HOST = '127.0.0.1'
PORT = 13854
ADDR = (HOST, PORT)
APP_NAME = 'Python'
USER_NAME = 'Anonymous'

# this is sent to the ThinkGearConnector to configure it to output json data
headset_conf_dict = {'enableRawOutput':False, 'format':'Json'}
# this is the character used by ThinkGearConnector to separate JSON objects
HEADSET_JSON_SEPARATOR = '\r'

# this is the data that the ThinkGearConnector sends out
brain_parameters = (
		lowAlpha, highAlpha, lowBeta, highBeta, 
		lowGamma, highGamma, delta, theta, 
		poorSignalLevel, meditation, attention) = (
		'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 
		'lowGamma', 'highGamma', 'delta', 'theta', 
		'poorSignalLevel', 'meditation', 'attention')
		
# these are the two general categories of brainwave data
parameter_categories = (eSense, eegPower) = ('eSense', 'eegPower')

# this is what data gets sent by the ThinkGearConnector before the headset connects
NULL_DATA = {poorSignalLevel:200}

def _extract_tuple(data_dict):
	"""Returns a tuple of the values extracted from a message dictionary."""
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
	"""Create a generator that will yield the data messages being sent by the ThinkGearConnector. """
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
		data = None
		try:
			data = json.loads(temp_json)
		except ValueError:
			print 'ValueError while trying to decode JSON object. discarding JSON that caused the error'
		if data:
			yield data
		else:
			continue
	cs.close()
	yield data
	
	
def _processDataStream(output_queue, shutdown_flag, connected_flag, host, port):
	"""Process the data coming in from the headset and load the processed data into a thread
	safe queue until the shutdown_flag is recognized as set."""
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
	"""An object that represents the brain of a user in a program. """
	
	def __init__(self, host=HOST, port=PORT, appName=APP_NAME, userName=USER_NAME):
		"""Initialize the brain by storing arguments, and setting up the threading model of the object."""
		self.queue = Queue.Queue()
		self.host = host
		self.port = port
		self.app_name = appName
		self.user_name = userName
		self.shutdown_stream = Event()
		self.is_connected_flag = Event()
		self.producer_thread = Thread(target=_processDataStream, args=(self.queue, self.shutdown_stream, self.is_connected_flag, host, port))
		self.freshest_data = {}
		self.producer_thread.start()

	def isConnected(self):
		"""Return True if the headset connection has been made and proper data is being received."""
		return self.is_connected_flag.isSet()
		
		
	def getProperty(self, propertyName):
		"""Return the most up to date data on the users brain wave activity."""
		if not self.queue.empty():
			self.freshest_data = self.queue.get(False)
		return self.freshest_data[propertyName] if propertyName in self.freshest_data else 0.0
		
	def __del__(self):
		"""Make sure that the producer thread has been shut down and allowed to terminate."""
		self.shutdown_stream.set()
		self.producer_thread.join()	
		
	def __str__(self):
		"""Generate a string giving basic info on the brain."""
		template = 'Brain:\n\tis connected: %s\n\thost: %s\tport: %d\n\tappName: %s\tuserName: %s'
		return template % (str(self.isConnected()), str(self.host), self.port, self.app_name, self.user_name)
		
	def fullstr(self):
		"""Generate a string giving the full information regarding the brain."""
		header = self.__str__() + '\n'
		for p in brain_parameters:
			header += '\t%s:\t%s\n' % (p, self.getProperty(p))
		return header

#def testBrain():
#	import code
#	my_brain = Brain()
#	while not my_brain.isConnected():
#		print 'brain not yet connected, trying again in 5 seconds'
#		time.sleep(5)
#	print 'brain now connected presumably, lets get some data'
#	print 'lowAlpha: %d\tattention: %f' % (my_brain.getProperty(lowAlpha), my_brain.getProperty(attention))
#	print 'sleep for 3 seconds then check again'
#	time.sleep(3)
#	print 'new data:'
#	print 'lowAlpha: %d\tattention: %f' % (my_brain.getProperty(lowAlpha), my_brain.getProperty(attention))
#	
#if __name__ == '__main__':
#	testBrain()