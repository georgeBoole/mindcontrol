from socket import *
import hashlib
import json

HOST = '127.0.0.1'
PORT = 13854
ADDR = (HOST, PORT)
cs = socket(AF_INET, SOCK_STREAM)
cs.connect(ADDR)

auth_dict = {'appName':'TestApp', 'appKey':hashlib.sha1().hexdigest()}
conf_dict = {'enableRawOutput':False, 'format':'Json'}
#cs.send(json.dumps(auth_dict))
cs.send(json.dumps(conf_dict))
#import code
#code.interact(local=locals())

while True:
	char = cs.recv(1)
	if char=='\r':
		print 'found delimiter'

cs.close()