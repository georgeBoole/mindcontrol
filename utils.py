#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by Michael Sobczak on 2012-07-26.
Copyright (c) 2012 Michael Sobczak. All rights reserved.
"""

def dict_string(d):
	lolstr = 'Dict: %s\n' % d
	for (k, v) in d.items():
		lolstr += '\tk: %s\tv: %s\n' % (k, v)
	return lolstr

