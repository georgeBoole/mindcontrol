from thinkgearlib import ThinkGearConnection
import threading
import Queue
from userbrain import _processDataStream, _extract_tuple, HOST, PORT, eSense, eegPower, brain_parameters
import time
from collections import defaultdict
import os
import sqlite3
import sys

def examine_results(qa, qb):
	# collect up and print all the a stuff
	results = defaultdict(list)
	for queue in [qa, qb]:
		while not queue.empty():
			results[queue].append(queue.get())
	import code
	code.interact(local=locals())
	
def dump_to_cvs(filename, keys, rows, should_append=False):
	f = open(filename, 'w')
	f.write(', '.join(keys) + '\n')
	for r in rows:
		o = ', '.join([str(x) for x in r]) + '\n'
		f.write(o)
	f.close()
	
def dump_to_db(db_filename, table_name, table_headers, table_rows):
	con = sqlite3.connect(db_filename)
	
	with con:
		cur = con.cursor()
		table_param_string = ', '.join( [ '%s REAL' % x for x in table_headers] )
		table_creation_string = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (table_name, table_param_string)
		cur.execute(table_creation_string)
		insert_template = 'INSERT INTO %s VALUES(%s)' % (table_name, ', '.join(['?'] * len(table_headers)))
		cur.executemany(insert_template, table_rows)
		

EXPERIMENT_RUNTIME = 60 # seconds
OUTPUT_FILE_NAME = 'experiment.csv'
DB_NAME = 'user_data.db'
TABLE_NAME = 'eeg_data'
USER_NAME = 'Michael'
APP_NAME = 'experiment'
def experiment():
	output_filename = OUTPUT_FILE_NAME
	#while os.path.isfile(output_filename):
	#	output_filename = 'a' + output_filename
	the_data = []
	tgc = ThinkGearConnection()
	data_started = False
	my_headers = brain_parameters
	start_time = 0
	for d in tgc.data():
		if eSense in d and eegPower in d:
			if not data_started:
				print 'Connection made, experiment started'
				data_started = True
				start_time = time.time()
			# real full message
			the_data.append(_extract_tuple(d))
		if data_started and time.time() - start_time > EXPERIMENT_RUNTIME:
			print 'Experiment over, exiting program'
			break
			
	print 'the_data: %s' % the_data
	print 'filename: %s' % output_filename
	print 'headers: %s' % ', '.join(my_headers)
	dump_to_db(DB_NAME, '%s_%s' % (APP_NAME.lower(), USER_NAME.lower()), my_headers, the_data)
if __name__ == '__main__':
	experiment()
