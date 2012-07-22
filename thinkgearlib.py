#!/usr/bin/env python
# encoding: utf-8
"""
thinkgearlib.py

Created by Michael Sobczak on 2012-07-21.
Copyright (c) 2012 Michael Sobczak. All rights reserved.
"""
from socket import *
import hashlib
import json
from speech import say

HOST = '127.0.0.1'
PORT = 13854
ADDR = (HOST, PORT)
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

printed_connecting = False
for d in datastream():
	
	if u'eSense' in d:
		#print 'attention: %f\tmeditation: %f' % (d[u'eSense'][u'attention'], d[u'eSense']['meditation'])
		print d
	else:
		if not printed_connecting:
			print 'connecting...'
			printed_connecting = True
	
