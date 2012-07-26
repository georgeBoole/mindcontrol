#!/usr/bin/env python
# encoding: utf-8
"""
thinkgearlib.py

Created by Michael Sobczak on 2012-07-21.
Copyright (c) 2012 Michael Sobczak. All rights reserved.
"""

"""
DEPRECATED!!! DONT USE THIS OMG
"""
from socket import *
import hashlib
import json
#from speech import say

HOST = '127.0.0.1'
PORT = 13854

#cs = socket(AF_INET, SOCK_STREAM)
#cs.connect(ADDR)

#auth_dict = {'appName':'TestApp', 'appKey':hashlib.sha1().hexdigest()}
conf_dict = {'enableRawOutput':False, 'format':'Json'}
#cs.send(json.dumps(auth_dict))
#cs.send(json.dumps(conf_dict))
#import code
#code.interact(local=locals())

#while True:
#	char = cs.recv(1)
#	if char=='\r':
#		print 'found delimiter'
#
#cs.close()
class ThinkGearConnection(object):
	
	def __init__(self, host=HOST, port=PORT, appName='Python', username='Anonymous'):
		self.host = host
		self.port = port
		self.appName = appName
		self.username = username
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.connect((self.host, self.port))
		self._sendMessage(conf_dict)
		self.recording = False
		self.is_running = True
		self.data_stream_active = False
			
	def data(self):
		self.data_stream_active = True
		my_data = None
		while self.is_running:
			temp_json = ''
			cur_char = self.sock.recv(1)
			while cur_char != '\r':
				temp_json += cur_char
				cur_char = self.sock.recv(1)
			my_data = json.decoder.JSONDecoder().decode(temp_json)
			yield my_data
		self.sock.close()
		self.data_stream_active = False
		
	def close(self):
		self.is_running = False		
		
	def setUser(self, userName):
		self._sendMessage({'setUser':{'userName':userName}})
		
	def getUsers(self):
		self._sendMessage({'getUsers':self.appName})
		
	def deleteUser(self, userName, userID):
		self._sendMessage({'deleteUser':{'userName':self.username, 'userId':userID}})
		
	def startRecording(self, rawEeg=True, poorSignalLevel=True, eSense=True, eegPower=True, blinkStrength=True):
		if self.data_stream_active:
			return
		self._sendMessage({'startRecording':{'rawEeg':rawEeg, 'poorSignalLevel':poorSignalLevel, 'sSense':eSense, 'eegPower':eegPower, 'blinkStrength':blinkStrength}, 'applicationName':self.appName})
		self.recording = True
		
	def stopRecording(self):
		if self.data_stream_active or not self.recording:
			return
		self._sendMessage({'stopRecording':self.appName})
		self.recording = False
		
	def cancelRecording(self):
		if self.data_stream_active or not self.recording:
			return
		self._sendMessage({'cancelRecording':self.appName})
		
	def getSessionIDs(self):
		self._sendMessage({'getSessionIds':self.appName})
		
	def retrieveSession(self, sessionID):
		self._sendMessage({'getSessionId':sessionID, 'applicationName':self.appName})
		
	def _sendMessage(self, messageDict):
		self.sock.send(json.dumps(messageDict))

def datastream(host=HOST, port=PORT):
	cs = socket(AF_INET, SOCK_STREAM)
	cs.connect((host, port))
	cs.send(json.dumps(conf_dict))
	data = None
	while True:
		temp_json = ''
		cur_char = cs.recv(1)
		while cur_char != '\r':
			temp_json += cur_char
			cur_char = cs.recv(1)
		data = json.decoder.JSONDecoder().decode(temp_json)
		yield data
		#if u'poorSignalLevel' in data and data[u'poorSignalLevel'] == 200:
		#	break
		#else:
		#	yield data 
	cs.close()
	yield data

#printed_connecting = False
#for d in datastream():
#	
#	if u'eSense' in d:
#		#print 'attention: %f\tmeditation: %f' % (d[u'eSense'][u'attention'], d[u'eSense']['meditation'])
#		print d
#	else:
#		if not printed_connecting:
#			print 'connecting...'
#			printed_connecting = True
	
#tgc = ThinkGearConnection()
#printed_connecting = False
#for d in tgc.data():
#	if u'eSense' in d:
#		if float(d[u'eSense'][u'meditation']) > 90:
#			say('High Meditation reached, exiting data collection')
#			tgc.close()
#	else:
#		print d
#
#say('Done with program')
