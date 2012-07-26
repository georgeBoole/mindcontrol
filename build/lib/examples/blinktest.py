#!/usr/bin/env python
# encoding: utf-8
"""
blinktest.py

Created by Michael Sobczak on 2012-07-24.
Copyright (c) 2012 Michael Sobczak. All rights reserved.
"""

from thinkgearlib import ThinkGearConnection

def capture_blinks(think_gear_connection, num_blinks):
	blink_count = 0
	blink_strength_list = []
	print('beginning capture of %d blinks' % num_blinks)
	while blink_count < num_blinks:
		print('please blink')
		event_data = think_gear_connection.data().next()
		while not u'blinkStrength' in event_data:
			event_data = think_gear_connection.data().next()
		blink_strength_list.append(event_data[u'blinkStrength'])
		blink_count += 1
		print event_data
		print('blink registered')
	return blink_strength_list

NUM_BLINKS = 3
NUM_ROUNDS = 4
def main():
	tcg = ThinkGearConnection()
	captured_blinks = [ capture_blinks(tcg, NUM_BLINKS) for x in xrange(NUM_ROUNDS) ]
	import code
	code.interact(local=locals())


if __name__ == '__main__':
	main()

