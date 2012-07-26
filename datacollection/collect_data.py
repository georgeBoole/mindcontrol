from mindcontrol.userbrain import *
#from collections import defaultdict
import sys

DEFAULT_CONFIG_FILE = 'default.cfg'
INVOCATION_ERROR_MESSAGE = 'No configuration file supplied. Will get configuration from user.'


def getUserInput(text_field_names):
	user_input = {}
	for f in text_field_names:
		user_input[f] = raw_input('%s: ' % f)
	return user_input
	
def runDataCollection(config_dict):
	#for d in BrainStream(lambda: False, )
	pass

def configureDataCollection(config_filename):
	#if not config_filename:
	pass
		
	
#if __name__ == '__main__':
#	#cfg = configureDataCollection()
#	fields = ('Name', 'Age', 'Hair Color')
#	ui = getUserInput(fields)
#	print ui
	
	
from sqlalchemy import *
from datetime import datetime

APP_NAME_LENGTH_MAX = 32

engine = create_engine('sqlite:///user_data.db')
metadata = MetaData()

def get_columns(headers):
	return [ Column(x, Float) for x in headers ]


eeg = Table('eeg', metadata,
	Column('app_name', String(APP_NAME_LENGTH_MAX)),
	Column('origin', Integer, ForeignKey('user.user_id')),
	Column('session_time', DateTime),
	Column('clock_time', DateTime, server_default=text('NOW()')),
	*get_columns(brain_parameters))
	
blink_event = Table('blink_event', metadata,
	Column('app_name', String(APP_NAME_LENGTH_MAX)),
	Column('origin', Integer, ForeignKey('user.user_id')),
	Column('session_time', DateTime),
	Column('clock_time', DateTime, server_default=text('NOW()')),
	Column('blinkStrength', Integer))

metadata.create_all(engine)

import code
code.interact(local=locals())
